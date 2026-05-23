CREATE TABLE dwd_zrr_gdjyxx_new (
    zrrwybs VARCHAR(800),
    sfzjhm VARCHAR(800),
    sfzjlx CHAR(16),
    xxwybs VARCHAR(48),
    xxmc VARCHAR(800),
    xh VARCHAR(48),
    rxrq DATE,
    byrq DATE,
    sxzy VARCHAR(48),
    xz CHAR(8),
    yxmc VARCHAR(800),
    njmc VARCHAR(400),
    bjmc VARCHAR(400),
    sfkns VARCHAR(400)
);

COMMENT ON TABLE dwd_zrr_gdjyxx_new IS '高等教育信息';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.xxwybs IS '学校唯一标识';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.xxmc IS '学校名称';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.xh IS '学号';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.rxrq IS '入学日期';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.byrq IS '毕业日期';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.sxzy IS '所学专业';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.xz IS '学制';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.yxmc IS '院系名称';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.njmc IS '年级名称';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.bjmc IS '班级名称';
COMMENT ON COLUMN dwd_zrr_gdjyxx_new.sfkns IS '是否困难生';