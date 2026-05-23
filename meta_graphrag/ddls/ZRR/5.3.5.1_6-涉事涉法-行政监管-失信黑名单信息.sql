CREATE TABLE dwd_zrr_sxhmdxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    sflrsxhmd INTEGER,
    lrsxhmdrq DATE,
    lrsxhmdsy VARCHAR(16000),
    tcsxhmdrq DATE,
    tcsxhmdyy VARCHAR(16000)
);

COMMENT ON TABLE dwd_zrr_sxhmdxx_new IS '失信黑名单信息';
COMMENT ON COLUMN dwd_zrr_sxhmdxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_sxhmdxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_sxhmdxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_sxhmdxx_new.sflrsxhmd IS '是否列入失信黑名单';
COMMENT ON COLUMN dwd_zrr_sxhmdxx_new.lrsxhmdrq IS '列入失信黑名单日期';
COMMENT ON COLUMN dwd_zrr_sxhmdxx_new.lrsxhmdsy IS '列入失信黑名单事由';
COMMENT ON COLUMN dwd_zrr_sxhmdxx_new.tcsxhmdrq IS '退出失信黑名单日期';
COMMENT ON COLUMN dwd_zrr_sxhmdxx_new.tcsxhmdyy IS '退出失信黑名单原因';