CREATE TABLE dwd_zrr_sxbzxxx_new (
    zrrwybs VARCHAR(1600),
    sfzjlx CHAR(400),
    sfzjhm VARCHAR(1600),
    sxxw VARCHAR(2000),
    sxbzxyjwh VARCHAR(2000),
    sxbzxrdrq DATE,
    sxbzxlarq DATE,
    sxbzxlxqk VARCHAR(160),
    serillrea_cn VARCHAR(1600),
    punishexecuteamount VARCHAR(2000),
    zxyj VARCHAR(2400)
);

COMMENT ON TABLE dwd_zrr_sxbzxxx_new IS '失信被执行信息';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.sxxw IS '失信行为';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.sxbzxyjwh IS '失信被执行依据文号';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.sxbzxrdrq IS '失信被执行认定日期';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.sxbzxlarq IS '失信被执行立案日期';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.sxbzxlxqk IS '失信被执行履行情况';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.serillrea_cn IS '列入事由/情形（中文名称）';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.punishexecuteamount IS '处罚执行金额/处罚金额';
COMMENT ON COLUMN dwd_zrr_sxbzxxx_new.zxyj IS '执行依据';