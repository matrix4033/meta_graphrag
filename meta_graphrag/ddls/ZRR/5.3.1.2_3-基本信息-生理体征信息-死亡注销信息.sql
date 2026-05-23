CREATE TABLE dwd_zrr_swzxxx_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    swrq DATE,
    swsj TIMESTAMP,
    swyy CHAR(24),
    swzxlx CHAR(8),
    swzxsj DATE,
    swzxjgmc VARCHAR(400)
);

COMMENT ON TABLE dwd_zrr_swzxxx_new IS '死亡注销信息';
COMMENT ON COLUMN dwd_zrr_swzxxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_swzxxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_swzxxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_swzxxx_new.swrq IS '死亡日期';
COMMENT ON COLUMN dwd_zrr_swzxxx_new.swsj IS '死亡时间';
COMMENT ON COLUMN dwd_zrr_swzxxx_new.swyy IS '死亡原因';
COMMENT ON COLUMN dwd_zrr_swzxxx_new.swzxlx IS '死亡注销类型';
COMMENT ON COLUMN dwd_zrr_swzxxx_new.swzxsj IS '死亡注销时间';
COMMENT ON COLUMN dwd_zrr_swzxxx_new.swzxjgmc IS '死亡注销机构名称';