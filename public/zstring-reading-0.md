---
title: ZStringを読もう
tags:
  - C#
  - OSS
private: false
updated_at: '2025-10-19T23:54:48+09:00'
id: 17b9c550e88c53678403
organization_url_name: null
slide: false
ignorePublish: false
---
どうもKutoです。
最近OSSを読みたいな欲が出てきまして、その第一歩として今回からZStringの読解を行っていきたいと思います。

## ZStringを選んだ理由
実際に読み始める前に、読むOSSを探した結果何故ZStringにしようと思ったのかの理由を簡潔に述べておこうと思います。
自分はつよつよエンジニアではありません。故にどんなOSSでも読めるというわけではなく、OSSを探す際にはいくつかの条件がありました。

* C#のOSSであること
  * 自分の一番得意な言語がC#であるため
* 使用者がそれなりにいること
    * 調べた際の情報量が多い方が読解は楽だろうと考えられるため
* 大きいOSSではないこと
    * .NET runtime などは到底読み切れないため

これらの条件のもと探した結果、一番適しているなと思ったのがZStringであったということです。加えて最近ゼロアロケーションについて調べていたというのもあり、最初のOSSをZStringに決めました。

ZStringはC#のライブラリを沢山作成されているCySharp産のライブラリです。日本産であることもあって日本語の記事も多く、比較的読みやすいのではないかと考えました。

## 記事一覧
1つの記事だけでは読み切れないため、PullRequest等の単位で記事を区切って読解していきたいと思います。
以下がその記事のリストです。随時更新します。

[ZStringを読もう(1)](https://qiita.com/kuto110/items/189cf89d26350fad800f)
[ZStringを読もう(2) initial commit](https://qiita.com/kuto110/items/541846a10b9a72890744)
[ZStringを読もう(3) Utf16ValuesStringBuilder.cs 最初の34行](https://qiita.com/kuto110/items/dc057f1e23b7e0ec2b0f)
