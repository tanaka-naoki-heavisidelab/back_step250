- .env について、コメント文は誤読の可能性があるため残さない。
  コメント文専用の.env.comment ファイルなどを置くと良い。
- .env 、 init.sql 、nginx.confについて、静的ファイルであるため外部から読み込めず、具体的な値をハードコピーするしかない。
- mysql/init.sql について、ユーザー名を.env の MYSQL_USER と一致させること。
