CREATE TABLE dwd_zrr_dkxx_new (
    zrrwybs VARCHAR(255),
    sfzjlx VARCHAR(255),
    sfzjhm VARCHAR(255),
    khyh VARCHAR(255),
    ffje NUMERIC,
    dklx VARCHAR(100)
);

COMMENT ON TABLE dwd_zrr_dkxx_new IS '贷款信息';
COMMENT ON COLUMN dwd_zrr_dkxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_dkxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_dkxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_dkxx_new.khyh IS '开户银行';
COMMENT ON COLUMN dwd_zrr_dkxx_new.ffje IS '发放金额';
COMMENT ON COLUMN dwd_zrr_dkxx_new.dklx IS '贷款类型';