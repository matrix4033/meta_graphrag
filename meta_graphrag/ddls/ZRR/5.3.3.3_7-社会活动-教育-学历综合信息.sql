CREATE TABLE dwd_zrr_xlzhxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx VARCHAR(160),
    sfzjhm VARCHAR(3000),
    xlmc VARCHAR(160),
    xlzy VARCHAR(48),
    xlsydw VARCHAR(800),
    xlsyrq DATE,
    xwlbm VARCHAR(400),
    xwmc VARCHAR(160),
    xwsydw VARCHAR(800),
    xwsyrq DATE
);

COMMENT ON TABLE dwd_zrr_xlzhxx_new IS '学历综合信息';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.xlmc IS '学历名称';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.xlzy IS '学历专业';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.xlsydw IS '学历授予单位';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.xlsyrq IS '学历授予日期';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.xwlbm IS '学位类别码';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.xwmc IS '学位名称';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.xwsydw IS '学位授予单位';
COMMENT ON COLUMN dwd_zrr_xlzhxx_new.xwsyrq IS '学位授予日期';