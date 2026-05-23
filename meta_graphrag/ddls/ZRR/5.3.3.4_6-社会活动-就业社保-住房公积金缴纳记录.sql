CREATE TABLE dwd_zrr_zfgjjjnjl_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    grzh CHAR(160),
    dwzh CHAR(160),
    jcjgh CHAR(160),
    jcjs NUMERIC,
    grjcje NUMERIC,
    dwjcje NUMERIC,
    jcbl VARCHAR(2000),
    grzhye NUMERIC,
    grzhzt VARCHAR(2000),
    dwmc VARCHAR(2000),
    hjyf CHAR(48),
    jcsj DATE
);

COMMENT ON TABLE dwd_zrr_zfgjjjnjl_new IS '住房公积金缴纳记录';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.grzh IS '个人账号';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.dwzh IS '单位账号';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.jcjgh IS '缴存机构号';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.jcjs IS '缴存基数';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.grjcje IS '个人缴存金额';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.dwjcje IS '单位缴存金额';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.jcbl IS '缴存比例';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.grzhye IS '个人账户余额';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.grzhzt IS '个人账户状态';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.dwmc IS '单位名称';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.hjyf IS '汇缴月份';
COMMENT ON COLUMN dwd_zrr_zfgjjjnjl_new.jcsj IS '缴存时间';