CREATE TABLE dwd_zrr_xzxk_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    xkwjlx VARCHAR(100),
    xkbfjg VARCHAR(100),
    xkbfrq DATE,
    xkzt VARCHAR(100),
    xkyxqz DATE,
    xkyxqzh DATE,
    xknr VARCHAR(4000)
);

COMMENT ON TABLE dwd_zrr_xzxk_new IS '行政许可';
COMMENT ON COLUMN dwd_zrr_xzxk_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xzxk_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xzxk_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xzxk_new.xkwjlx IS '许可文件类型';
COMMENT ON COLUMN dwd_zrr_xzxk_new.xkbfjg IS '许可颁发机关';
COMMENT ON COLUMN dwd_zrr_xzxk_new.xkbfrq IS '许可颁发日期';
COMMENT ON COLUMN dwd_zrr_xzxk_new.xkzt IS '许可状态';
COMMENT ON COLUMN dwd_zrr_xzxk_new.xkyxqz IS '许可有效期自';
COMMENT ON COLUMN dwd_zrr_xzxk_new.xkyxqzh IS '许可有效期至';
COMMENT ON COLUMN dwd_zrr_xzxk_new.xknr IS '许可内容';