// currently working on TGCOffice/Objects.level.bin

struct unk1 {
    u32;
    u8;
    u8;
    padding[2];
    u32;
    u32;
};

struct string {
    char x[];
};

struct BstNode {
    char name[];
    u32 numProps;
    u32 props[numProps];
    u32;
};

struct Level {
    char fourcc[4];
    u32;
    u32;
    u32;
    u32;
    u32;
    u32;
    u32 i;
//    u32 j[i / sizeof(u32)];
    u32 j[0x410 / 4 - 4];
    unk1 k[(0x3f80-0x430) / sizeof(unk1)];
    string propNames[760];
    padding[4];
    BstNode;
    BstNode;
};

Level level @ 0x0;

