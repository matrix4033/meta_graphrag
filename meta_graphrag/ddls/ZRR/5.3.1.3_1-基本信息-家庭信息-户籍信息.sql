CREATE TABLE dwd_zrr_hjxx_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    jg VARCHAR(100),
    hklb VARCHAR(20),
    hjszd VARCHAR(200),
    hjdssxdm VARCHAR(100),
    hjdxz VARCHAR(2000),
    hjdjlxdm VARCHAR(40),
    hzxm VARCHAR(100),
    hzsfhm VARCHAR(100),
    hjqfdw VARCHAR(50),
    hjqfsj DATE,
    hjzxbs VARCHAR(20),
    hjzxrq DATE
);

COMMENT ON TABLE dwd_zrr_hjxx_new IS '户籍信息';
COMMENT ON COLUMN dwd_zrr_hjxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_hjxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_hjxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_hjxx_new.jg IS '籍贯';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hklb IS '户口类别';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hjszd IS '户籍所在地';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hjdssxdm IS '户籍地省市县代码';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hjdxz IS '户籍地详址';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hjdjlxdm IS '户籍地街路巷代码';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hzxm IS '户主姓名';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hzsfhm IS '户主身份号码';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hjqfdw IS '户籍签发单位';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hjqfsj IS '户籍签发时间';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hjzxbs IS '户籍注销标识';
COMMENT ON COLUMN dwd_zrr_hjxx_new.hjzxrq IS '户籍注销日期';