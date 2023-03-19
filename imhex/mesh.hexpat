#pragma pattern_limit 1048576

struct Vec3Padded {
    float x;
    float y;
    float z;
    padding[4];
};

struct Vec3 {
    float x;
    float y;
    float z;
};

struct Vec2Padded {
    // Actually half-precision floats
    u16 x;
    u16 y;
    padding[12];
};

struct Vec2 {
    float x;
    float y;
};

// Unverified
struct BoneWeight {
    u16 bone;
    float weight;
};

struct Face<T> {
    T idx[3];
};

struct MeshLod {
    // Assumes mesh header was lost as part of the
    // decompression process.

    // Sometimes set to inf. This is fine - this is
    // supposed to be an override for an unknown value
    float;

    // Axis-aligned bounding box
    Vec3 aabbA;
    Vec3 aabbB;

    // for mesh version >= 0x1c
        // Usually a copy of the AABB
        Vec3 aabbA_2;
        Vec3 aabbB_2;
    // for mesh version > 0x1c
        padding[0x20];
        padding[0x20];

    u32 sharedVertices;
    u32 totalVertices;

    // for mesh version >= 0x1e
        u32 isIdx32;

    u32 numPoints;
    u32 prop11;
    u32 prop12;
    u32 prop13;
    u32 prop14;
    // for mesh version >= 0x1d
        u8 loadMeshNorms; // if set, load mesh normals
        u8 loadInfo2;
        u8 loadInfo3;
        u32 skipMeshPos; // if zero, load mesh positions
        u32 skipUvs; // if zero, load UV coords
        u32 flag3;
    u8 unk[0x10];
    if (skipMeshPos == 0) { // or mesh version < 0x1d
        Vec3Padded vtxBuffer[sharedVertices];
    }
    if (loadMeshNorms) {
        float normals[sharedVertices];
    }
    if (skipUvs == 0) { // or mesh version < 0x1d
        Vec2Padded uvBuffer[sharedVertices];
    }
    if (false) { // if animated
        BoneWeight animWeights[sharedVertices];
    }
    
    if (!isIdx32) {
        Face<u16> idxBuffer[totalVertices / 3];
    } else {
        Face<u32> idxBuffer[totalVertices / 3];
    }
    
    if (loadInfo2) {
        if (!isIdx32) {
            // Likely densities
            u8 miscData1[totalVertices * 2];
        } else {
            u8 miscData1[totalVertices * 4];
        }
    }

    if (numPoints > 0) {
        if (!isIdx32) {
            u8 miscData2[sharedVertices * 2];
        } else {
            u8 miscData2[sharedVertices * 4];
        }
    }
    
    if (prop11 > 0) {
        if (!isIdx32) {
            u8 miscData3[sharedVertices * 2];
        } else {
            u8 miscData3[sharedVertices * 4];
        }
    }

    if (prop12 > 0) {
        if (!isIdx32) {
            u8 miscData4[prop12 * 2];
        } else {
            u8 miscData4[prop12 * 4];
        }
    }
    
    if (prop13 > 0) {
        u8 miscData5[prop13 * 4];
    }
    
    if (prop14 > 0) {
        if (!isIdx32) {
            u8 miscData6[prop14 * 4];
        } else {
            u8 miscData6[prop14 * 8];
        }
    }
    
    u8 miscData7[(totalVertices / 3) * 4];
    
    if (skipMeshPos) {
        u8 altPosData1[sharedVertices * 4];
        u8 altPosData2[sharedVertices];
    }
    
    if (skipUvs) {
        u8 altUvData[sharedVertices * 4];
    }
    
    if (flag3) {
        u8 altFlag3Data[sharedVtxCnt * 4];
    }
};

struct OcclusionData {
    u32 f1;
    u32 f2;
    u8 arr1[f1 * 3 * 4];
    u8 arr2[f2 * 4];
};

struct Mesh {
    MeshLod lods[];
    OcclusionData;
};

MeshLod mesh @ 0x0;


