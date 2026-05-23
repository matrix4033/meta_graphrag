CREATE TABLE dwd_zrr_swyxzmxx_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    swrq DATE,
    swsj TIMESTAMP,
    swyy CHAR(24),
    swzmfzjg VARCHAR(400),
    swzmqmz VARCHAR(4000)
);

COMMENT ON TABLE dwd_zrr_swyxzmxx_new IS '死亡医学证明信息';
COMMENT ON COLUMN dwd_zrr_swyxzmxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_swyxzmxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_swyxzmxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_swyxzmxx_new.swrq IS '死亡日期';
COMMENT ON COLUMN dwd_zrr_swyxzmxx_new.swsj IS '死亡时间';
COMMENT ON COLUMN dwd_zrr_swyxzmxx_new.swyy IS '死亡原因';
COMMENT ON COLUMN dwd_zrr_swyxzmxx_new.swzmfzjg IS '死亡证明发证机关';
COMMENT ON COLUMN dwd_zrr_swyxzmxx_new.swzmqmz IS '死亡证明编号';