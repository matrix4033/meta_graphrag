CREATE TABLE dwd_zrr_sfajxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx VARCHAR(16),
    sfzjhm VARCHAR(800),
    sfajah VARCHAR(800),
    sfajahdm VARCHAR(800),
    sfajygr VARCHAR(800),
    sfajay VARCHAR(2400),
    sfajlarq DATE,
    sfajpjg VARCHAR(2560),
    zxajbjrq DATE,
    zxajjafs VARCHAR(2000),
    sfajbgr VARCHAR(800),
    bgsfzjhm VARCHAR(800),
    fymc VARCHAR(200),
    ajlx VARCHAR(200)
);

COMMENT ON TABLE dwd_zrr_sfajxx_new IS '司法案件信息';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.sfajah IS '司法案件案号';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.sfajahdm IS '司法案件案号代码';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.sfajygr IS '司法案件原告人';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.sfajay IS '司法案件案由';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.sfajlarq IS '司法案件立案日期';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.sfajpjg IS '司法案件判决结果';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.zxajbjrq IS '执行案件报结日期';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.zxajjafs IS '执行案件结案方式';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.sfajbgr IS '司法案件被告人';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.bgsfzjhm IS '被告身份证件号码';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.fymc IS '法院名称';
COMMENT ON COLUMN dwd_zrr_sfajxx_new.ajlx IS '案件类型';