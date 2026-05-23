CREATE TABLE dwd_zrr_ywjyxx_new (
    zrrwybs VARCHAR(800),
    sfzjlx VARCHAR(200),
    sfzjhm VARCHAR(800),
    xxwybs VARCHAR(800),
    xh VARCHAR(800),
    njmc VARCHAR(400),
    bjmc VARCHAR(400),
    xxmc VARCHAR(255)
);

COMMENT ON TABLE dwd_zrr_ywjyxx_new IS '义务教育信息';
COMMENT ON COLUMN dwd_zrr_ywjyxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_ywjyxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_ywjyxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_ywjyxx_new.xxwybs IS '学校唯一标识';
COMMENT ON COLUMN dwd_zrr_ywjyxx_new.xh IS '学号';
COMMENT ON COLUMN dwd_zrr_ywjyxx_new.njmc IS '年级名称';
COMMENT ON COLUMN dwd_zrr_ywjyxx_new.bjmc IS '班级名称';
COMMENT ON COLUMN dwd_zrr_ywjyxx_new.xxmc IS '学校名称';