CREATE TABLE dwd_zrr_zyjyxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(2000),
    xxwys VARCHAR(3000),
    xh VARCHAR(800),
    rxrq DATE,
    byrq DATE,
    sxzy VARCHAR(50),
    xz CHAR(50),
    njmc VARCHAR(200),
    bjmc VARCHAR(200),
    xxmc VARCHAR(800)
);

COMMENT ON TABLE dwd_zrr_zyjyxx_new IS '职业教育信息';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.xxwys IS '学校唯一标识';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.xh IS '学号';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.rxrq IS '入学日期';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.byrq IS '毕业日期';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.sxzy IS '所学专业';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.xz IS '学制';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.njmc IS '年级名称';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.bjmc IS '班级名称';
COMMENT ON COLUMN dwd_zrr_zyjyxx_new.xxmc IS '学校名称';