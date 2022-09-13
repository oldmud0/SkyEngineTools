import ctypes
import struct
import io
from ctypes import *

filename = '/tmp/AncestorStatueDawn_01.mesh'
f = open(filename, 'rb')

lz4 = CDLL('liblz4.so.1')

# read uncompressed size
f.seek(0x52)
uncompressed_size = struct.unpack('i', f.read(4))[0]

# read compressed size
f.seek(0x4e)
compressed_size = struct.unpack('i', f.read(4))[0]

# read num lods
f.seek(0x44)
num_lods = struct.unpack('i', f.read(4))[0]

print('compressed_size', compressed_size)
print('uncompressed_size', uncompressed_size)
print('num_lods', num_lods)

# get compressed content
f.seek(0x56)
src = f.read(compressed_size)

# get decompressed content
dest = ctypes.create_string_buffer(uncompressed_size)
ret = lz4.LZ4_decompress_safe(src, dest, compressed_size, uncompressed_size)
if ret <= 0:
    raise IOError('error decompressing mesh - file may not be valid')

o = open(f'{filename}.bin', 'wb')
o.write(dest.raw)
o.close()

buf = io.BytesIO(dest.raw)
buf.seek(0x74)
shared_vertex_count = struct.unpack('i', buf.read1(4))[0]
buf.seek(0x78)
total_vertex_count = struct.unpack('i', buf.read1(4))[0]
buf.seek(0x80)
point_count = struct.unpack('i', buf.read1(4))[0]
buf.seek(0x74)
uv_count = struct.unpack('i', buf.read1(4))[0]

print('shared_vertex_count', shared_vertex_count)
print('total_vertex_count', total_vertex_count)
print('point_count', point_count)
print('uv_count', uv_count)

# build vertex buffer
vertex_buffer = []
vertex_buffer_start = 0xb3
buf.seek(vertex_buffer_start)

for i in range(shared_vertex_count):
    # 3 floats
    x, y, z = struct.unpack('<fff4x', buf.read(16))
    vertex_buffer.append((x, y, z))

# build uv buffer
uv_buffer = []
uv_header_size = uv_count * 4 - 4
buf.read1(uv_header_size) # move caret to uv start
for i in range(uv_count):
    # 2 half-precision floats
    u, v = struct.unpack('<4xee8x', buf.read(16))
    uv_buffer.append((u, v))

# build index buffer
index_buffer = []
face_count = total_vertex_count // 3
buf.read1(4) # advance 4 bytes of padding
for i in range(face_count):
    # 3 shorts (each indexing into the vertex buffer)
    v1, v2, v3 = struct.unpack('<HHH', buf.read(6))
    index_buffer.append((v1, v2, v3))

f.close()
buf.close()

# print(vertex_buffer)
# print(index_buffer)

# build geometry from buffers
vertices = []
edges = []
faces = []
for face in index_buffer:
    v1i, v2i, v3i = face
    edges += [(v1i, v2i), (v2i, v3i), (v3i, v1i)]
    faces.append(face)

try:
    import bpy
except:
    print('not in Blender, exiting now')
    exit()
mesh = bpy.data.meshes.new('created_mesh')
mesh.from_pydata(vertex_buffer, edges, faces)
mesh.update()

uvl = mesh.uv_layers.new()
uvl.data.foreach_set('uv', [uv for pair in [uv_buffer[l.vertex_index] for l in mesh.loops] for uv in pair])
mesh.uv_layers.active = uvl

obj = bpy.data.objects.new('created_object', mesh)
collection = bpy.data.collections.new('created_collection')
bpy.context.scene.collection.children.link(collection)
collection.objects.link(obj)