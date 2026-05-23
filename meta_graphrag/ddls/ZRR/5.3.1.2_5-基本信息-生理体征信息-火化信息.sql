CREATE TABLE dwd_zrr_hhxx_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    swrq DATE,
    swsj TIMESTAMP,
    swyy CHAR(24),
    hhzjbh VARCHAR(512),
    hhrq DATE,
    hhszbyg VARCHAR(800)
);

COMMENT ON TABLE dwd_zrr_hhxx_new IS '火化信息';
COMMENT ON COLUMN dwd_zrr_hhxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_hhxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_hhxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_hhxx_new.swrq IS '死亡日期';
COMMENT ON COLUMN dwd_zrr_hhxx_new.swsj IS '死亡时间';
COMMENT ON COLUMN dwd_zrr_hhxx_new.swyy IS '死亡原因';
COMMENT ON COLUMN dwd_zrr_hhxx_new.hhzjbh IS '火化证件编号';
COMMENT ON COLUMN dwd_zrr_hhxx_new.hhrq IS '火化日期';
COMMENT ON COLUMN dwd_zrr_hhxx_new.hhszbyg IS '火化所在殡仪馆';