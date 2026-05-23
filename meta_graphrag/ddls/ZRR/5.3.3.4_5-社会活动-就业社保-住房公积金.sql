CREATE TABLE dwd_zrr_zfgjj_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(3000),
    zfgjjzh CHAR(50),
    zfgjjdwzh CHAR(100),
    zfgjjjcjgh CHAR(500),
    zfgjjkhrq DATE,
    zfgjjzhzt CHAR(50),
    zfgjjjcjs NUMERIC
);

COMMENT ON TABLE dwd_zrr_zfgjj_new IS '住房公积金';
COMMENT ON COLUMN dwd_zrr_zfgjj_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_zfgjj_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_zfgjj_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_zfgjj_new.zfgjjzh IS '住房公积金账号';
COMMENT ON COLUMN dwd_zrr_zfgjj_new.zfgjjdwzh IS '住房公积金单位账号';
COMMENT ON COLUMN dwd_zrr_zfgjj_new.zfgjjjcjgh IS '住房公积金缴存机构号';
COMMENT ON COLUMN dwd_zrr_zfgjj_new.zfgjjkhrq IS '住房公积金开户日期';
COMMENT ON COLUMN dwd_zrr_zfgjj_new.zfgjjzhzt IS '住房公积金账户状态';
COMMENT ON COLUMN dwd_zrr_zfgjj_new.zfgjjjcjs IS '住房公积金缴存基数';