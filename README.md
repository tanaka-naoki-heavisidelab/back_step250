- .env ファイルについて、コメント文は誤読の可能性があるため残さない。
  コメント文専用の.env.comment ファイルなどを置くと良い。
- .env ファイルと init.sql について、静的ファイルであるため.env から読み込めない。
  　ハードコピーするしかない。
- mysql/init.sql について、ユーザー名を.env の MYSQL_USER と一致させること。
