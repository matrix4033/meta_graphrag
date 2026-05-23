CREATE TABLE dwd_zrr_syxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(3000),
    djsyrq DATE,
    syyy VARCHAR(4000),
    jyknlb CHAR(40),
    jycyzbh VARCHAR(240),
    jycyzfzjg VARCHAR(800)
);

COMMENT ON TABLE dwd_zrr_syxx_new IS '失业信息';
COMMENT ON COLUMN dwd_zrr_syxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_syxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_syxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_syxx_new.djsyrq IS '登记失业日期';
COMMENT ON COLUMN dwd_zrr_syxx_new.syyy IS '失业原因';
COMMENT ON COLUMN dwd_zrr_syxx_new.jyknlb IS '就业困难类别';
COMMENT ON COLUMN dwd_zrr_syxx_new.jycyzbh IS '就业创业证编号';
COMMENT ON COLUMN dwd_zrr_syxx_new.jycyzfzjg IS '就业创业证发证机构';