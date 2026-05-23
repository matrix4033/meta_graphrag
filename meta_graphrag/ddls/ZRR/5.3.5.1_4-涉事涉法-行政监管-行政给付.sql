CREATE TABLE dwd_zrr_xzjf_new (
    zrrwybs VARCHAR(200),
    sfzjlx VARCHAR(100),
    sfzjhm VARCHAR(200),
    xzgfsx VARCHAR(2000),
    xzgfshjg VARCHAR(1000),
    xzgffy VARCHAR(300),
    xzgfrq VARCHAR(30)
);

COMMENT ON TABLE dwd_zrr_xzjf_new IS '行政给付';
COMMENT ON COLUMN dwd_zrr_xzjf_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xzjf_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xzjf_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xzjf_new.xzgfsx IS '行政给付事项';
COMMENT ON COLUMN dwd_zrr_xzjf_new.xzgfshjg IS '行政给付审核结果';
COMMENT ON COLUMN dwd_zrr_xzjf_new.xzgffy IS '行政给付费用';
COMMENT ON COLUMN dwd_zrr_xzjf_new.xzgfrq IS '行政给付日期';