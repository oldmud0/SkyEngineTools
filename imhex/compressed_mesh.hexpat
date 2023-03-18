struct CompressedMesh {
	u32 version;
	// First 64 bytes are dumped into the MeshData
	// struct in memory, but not fully convinced
	// that it's all just for the name.
	char name[0x40];
	u32 numLods;
	u8 animated;
	u8 hasOcclusionMesh;
	u32 compressed;
	if (compressed) {
	   u32 compressedSize;
       u32 uncompressedSize;
       // LZ4 compressed
       u8 compressedBytes[compressedSize];
	}
};

CompressedMesh mesh @ 0x0;
