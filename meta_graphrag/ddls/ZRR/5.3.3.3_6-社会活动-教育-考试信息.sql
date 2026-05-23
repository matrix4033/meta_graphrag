CREATE TABLE dwd_zrr_ksxx_new (
    zrrwybs VARCHAR(800),
    sfzjhm VARCHAR(800),
    sfzjlx CHAR(16),
    byrq DATE,
    bylx VARCHAR(2040),
    byzhm VARCHAR(2040),
    dxbyscc VARCHAR(2040),
    ksh VARCHAR(2040),
    kmdm VARCHAR(2040),
    kmmc VARCHAR(2040),
    ksrq DATE,
    kscj VARCHAR(2040)
);

COMMENT ON TABLE dwd_zrr_ksxx_new IS '考试信息';
COMMENT ON COLUMN dwd_zrr_ksxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_ksxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_ksxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_ksxx_new.byrq IS '毕业日期';
COMMENT ON COLUMN dwd_zrr_ksxx_new.bylx IS '毕业类型';
COMMENT ON COLUMN dwd_zrr_ksxx_new.byzhm IS '毕业证号码';
COMMENT ON COLUMN dwd_zrr_ksxx_new.dxbyscc IS '大学毕业生层次';
COMMENT ON COLUMN dwd_zrr_ksxx_new.ksh IS '考生号';
COMMENT ON COLUMN dwd_zrr_ksxx_new.kmdm IS '科目代码';
COMMENT ON COLUMN dwd_zrr_ksxx_new.kmmc IS '科目名称';
COMMENT ON COLUMN dwd_zrr_ksxx_new.ksrq IS '考试日期';
COMMENT ON COLUMN dwd_zrr_ksxx_new.kscj IS '考试成绩';