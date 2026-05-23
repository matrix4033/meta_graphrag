CREATE TABLE dwd_zrr_gzjyxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(100),
    sfzjhm VARCHAR(2000),
    xxwys VARCHAR(3000),
    xh VARCHAR(1000),
    njmc VARCHAR(1000),
    bjmc VARCHAR(1000),
    xxmc VARCHAR(800)
);

COMMENT ON TABLE dwd_zrr_gzjyxx_new IS '高中教育信息';
COMMENT ON COLUMN dwd_zrr_gzjyxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_gzjyxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_gzjyxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_gzjyxx_new.xxwys IS '学校唯一标识';
COMMENT ON COLUMN dwd_zrr_gzjyxx_new.xh IS '学号';
COMMENT ON COLUMN dwd_zrr_gzjyxx_new.njmc IS '年级名称';
COMMENT ON COLUMN dwd_zrr_gzjyxx_new.bjmc IS '班级名称';
COMMENT ON COLUMN dwd_zrr_gzjyxx_new.xxmc IS '学校名称';