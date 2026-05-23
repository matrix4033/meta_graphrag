CREATE TABLE dwd_zrr_fcxx_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    fwdz VARCHAR(1600),
    fwxz VARCHAR(800),
    fwjzmj NUMERIC,
    fwsymj NUMERIC,
    fwmc VARCHAR(800),
    fwfh VARCHAR(800),
    gfhtqdrq DATE
);

COMMENT ON TABLE dwd_zrr_fcxx_new IS '房产信息';
COMMENT ON COLUMN dwd_zrr_fcxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_fcxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_fcxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_fcxx_new.fwdz IS '房屋地址';
COMMENT ON COLUMN dwd_zrr_fcxx_new.fwxz IS '房屋性质';
COMMENT ON COLUMN dwd_zrr_fcxx_new.fwjzmj IS '房屋建筑面积';
COMMENT ON COLUMN dwd_zrr_fcxx_new.fwsymj IS '房屋使用面积';
COMMENT ON COLUMN dwd_zrr_fcxx_new.fwmc IS '房屋名称';
COMMENT ON COLUMN dwd_zrr_fcxx_new.fwfh IS '房屋房号';
COMMENT ON COLUMN dwd_zrr_fcxx_new.gfhtqdrq IS '购房合同签订日期';