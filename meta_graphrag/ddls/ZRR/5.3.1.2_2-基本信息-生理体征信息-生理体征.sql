CREATE TABLE dwd_zrr_sltz_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    jkzk CHAR(8),
    tz NUMERIC,
    sg NUMERIC,
    cjzh VARCHAR(500),
    cjlx CHAR(16),
    cjdj VARCHAR(80)
);

COMMENT ON TABLE dwd_zrr_sltz_new IS '生理体征';
COMMENT ON COLUMN dwd_zrr_sltz_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_sltz_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_sltz_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_sltz_new.jkzk IS '健康状况';
COMMENT ON COLUMN dwd_zrr_sltz_new.tz IS '体重';
COMMENT ON COLUMN dwd_zrr_sltz_new.sg IS '身高';
COMMENT ON COLUMN dwd_zrr_sltz_new.cjzh IS '残疾证号';
COMMENT ON COLUMN dwd_zrr_sltz_new.cjlx IS '残疾类型';
COMMENT ON COLUMN dwd_zrr_sltz_new.cjdj IS '残疾等级';