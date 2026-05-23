CREATE TABLE dwd_zrr_xifxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    sfrsfzm VARCHAR(400),
    xfrq DATE,
    xfsj VARCHAR(16000),
    xfsy VARCHAR(16000),
    xfbm VARCHAR(160),
    wqnr VARCHAR(16000),
    wqrq DATE
);

COMMENT ON TABLE dwd_zrr_xifxx_new IS '信访信息';
COMMENT ON COLUMN dwd_zrr_xifxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xifxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xifxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xifxx_new.sfrsfzm IS '上访人身份证明';
COMMENT ON COLUMN dwd_zrr_xifxx_new.xfrq IS '信访日期';
COMMENT ON COLUMN dwd_zrr_xifxx_new.xfsj IS '信访事件';
COMMENT ON COLUMN dwd_zrr_xifxx_new.xfsy IS '信访事由';
COMMENT ON COLUMN dwd_zrr_xifxx_new.xfbm IS '信访部门';
COMMENT ON COLUMN dwd_zrr_xifxx_new.wqnr IS '维权内容';
COMMENT ON COLUMN dwd_zrr_xifxx_new.wqrq IS '维权日期';