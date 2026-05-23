CREATE TABLE dwd_zrr_wlxsxcpqk_new (
    zrrwybs VARCHAR(255),
    sfzjlx VARCHAR(25),
    sfzjhm VARCHAR(255),
    ah VARCHAR(255),
    zczxyjdw VARCHAR(800),
    sxbzxrxm VARCHAR(800),
    lasj DATE,
    flsxwsqddyw VARCHAR(800),
    fbsj DATE,
    bzxrdlxqk VARCHAR(16000),
    sxbzxrjtqx VARCHAR(16000),
    wlxbf VARCHAR(2400)
);

COMMENT ON TABLE dwd_zrr_wlxsxcpqk_new IS '未履行生效裁判信息';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.ah IS '案号';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.zczxyjdw IS '作出执行依据单位';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.sxbzxrxm IS '被执行人姓名';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.lasj IS '立案时间';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.flsxwsqddyw IS '法律生效文书确定的义务';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.fbsj IS '发布时间';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.bzxrdlxqk IS '被执行人的履行情况';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.sxbzxrjtqx IS '失信被执行人具体情况';
COMMENT ON COLUMN dwd_zrr_wlxsxcpqk_new.wlxbf IS '未履行部分';