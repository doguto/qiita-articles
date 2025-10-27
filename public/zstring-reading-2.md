---
title: ZStringを読もう(2) initial commit
tags:
  - C#
  - OSS
private: false
updated_at: '2025-10-19T23:56:29+09:00'
id: 541846a10b9a72890744
organization_url_name: null
slide: false
ignorePublish: false
---
どうもKutoです。
ということで、ZStringを読もうの第2回です。
前回はZStringの概要の説明を行いましたが、今回から実際にコードリーディングを始めていきたいと思います。

## 利用ツール

* Rider
* copilot cli

今回は以上のツールを使用してコードを読んでいきたいと思います。
VScodeの環境構築が面倒なため、私はC#を書くときには基本的にRiderを使用しています。非商用利用は無料ですからね。
加えて今回はコードの読解時に分からない部分を聞くため、copilot cliを使用したいと思います。chat-gpt等でも良いのですが、agentで実際にコードベースを確認しながら回答してくれるのでより精度が期待できるためです。
それではツールの紹介も終わったところで、早速コードを見ていきましょう

## initial commit

最初から最新のコードを読んでも良いのですが、今回はinitial commitから順番にコードを読んでいきたいと思います。
最新はコード量がどうしても多いですからね。一度に読む単位は極力小さくしたいです。
initial commitだけは例外的に複数記事またぎますが、以降はPullRequest単位等で変更を追って行く予定です。

cloneしてコードを持ってきたのち、initial commitへとcheckoutしていきます。

```sh
git checkout $(git rev-list --max-parents=0 HEAD)
```

## ディレクトリ構造

まずはディレクトリ構造をざっと眺めていきたいと思います。
initial commitの段階ではそこまでファイル数が多くないので、一覧で全て出すことができますね。

```
ZString/
├── .circleci/
│   └── config.yml
├── sandbox/
│   ├── ConsoleApp/
│   │   ├── ConsoleApp.csproj
│   │   └── Program.cs
│   └── PerfBenchmark/
├── src/
│   └── ZString/
│       ├── Utf16/
│       │   ├── Utf16ValueStringBuilder.AppendFormat.cs
│       │   ├── Utf16ValueStringBuilder.AppendFormat.tt
│       │   ├── Utf16ValueStringBuilder.AppendMany.cs
│       │   ├── Utf16ValueStringBuilder.AppendMany.tt
│       │   ├── Utf16ValueStringBuilder.CreateFormatter.cs
│       │   ├── Utf16ValueStringBuilder.CreateFormatter.tt
│       │   ├── Utf16ValueStringBuilder.SpanFormattableAppend.cs
│       │   └── Utf16ValueStringBuilder.SpanFormattableAppend.tt
│       ├── Utf8/
│       │   ├── Utf8ValueStringBuilder.AppendFormat.cs
│       │   ├── Utf8ValueStringBuilder.AppendFormat.tt
│       │   ├── Utf8ValueStringBuilder.AppendMany.cs
│       │   ├── Utf8ValueStringBuilder.AppendMany.tt
│       │   ├── Utf8ValueStringBuilder.CreateFormatter.cs
│       │   ├── Utf8ValueStringBuilder.CreateFormatter.tt
│       │   ├── Utf8ValueStringBuilder.SpanFormattableAppend.cs
│       │   └── Utf8ValueStringBuilder.SpanFormattableAppend.tt
│       ├── FormatParser.cs
│       ├── Utf16ValueStringBuilder.cs
│       ├── Utf8ValueStringBuilder.cs
│       ├── ZString.cs
│       ├── ZString.csproj
│       ├── ZString.Format.cs
│       └── ZString.Format.tt
├── tests/
│   └── ZString.Tests/
│       ├── FormatTest.cs
│       └── ZString.Tests.csproj
├── .gitignore
├── LICENSE
├── README.md
└── ZString.sln
```

今回は基本的に内部実装を見ていきたいため、`.circleci`や`sandbox`等は見ていきません。`src/`のみを読んでいきたいと思います。
そして`src/`に関して見てみると、`ZString.cs`という大本のファイルがあり、その他具体的なロジックファイルがUtf8とUtf16に対して分けて用意されていることが分かります。

<details>
  <summary>UTF-8・UTF-16とは？</summary>
  Chat-GPTの解答を示しておこうと思います。

  ## 🔤 文字コードとは

  まず前提として、**コンピュータは文字を直接理解できない**ので、文字を「数値」に変換して保存・通信します。
  この「文字 → 数値」の対応ルールが **文字コード（エンコーディング）** です。

  その中でも有名なのが
  ➡️ **UTF-8**
  ➡️ **UTF-16**
  です。どちらも **Unicode** という国際的な文字セットを使います。

  ---

  ## 🧩 Unicodeとは？

  Unicodeは、世界中の文字（日本語・英語・絵文字など）に一意な番号（コードポイント）を割り当てた仕組みです。

  例：

  | 文字 | Unicodeコードポイント |
  | -- | -------------- |
  | A  | U+0041         |
  | あ  | U+3042         |
  | 😃 | U+1F603        |

  ---

  ## ⚙️ UTF-8 と UTF-16 の違い

  | 特徴            | UTF-8                 | UTF-16                |
  | ------------- | --------------------- | --------------------- |
  | エンコーディング単位    | 1バイトごと（8ビット）          | 2バイトごと（16ビット）         |
  | 可変長 or 固定長    | **可変長（1〜4バイト）**       | **可変長（2または4バイト）**     |
  | ASCII文字（英数字）  | **1バイトで表現可能**（超効率的）   | **2バイト固定**（少し無駄）      |
  | 日本語など非ASCII文字 | 3バイト                  | 2バイト（または4バイト）         |
  | 主な利用場所        | Web、Linux、JSON、HTMLなど | Windows、.NET、Java内部など |
  | メリット          | 英語中心のデータが軽い           | 国際文字を扱うとき効率的          |
  | デメリット         | 日本語や絵文字が多いと重くなる       | 英語中心だと無駄が多い           |

  ---

  ## 🔍 具体例（文字列「Aあ😃」の場合）

  | 文字     | UTF-8 (16進) | バイト数 | UTF-16 (16進) | バイト数 |
  | ------ | ----------- | ---- | ------------ | ---- |
  | A      | 41          | 1    | 0041         | 2    |
  | あ      | E3 81 82    | 3    | 3042         | 2    |
  | 😃     | F0 9F 98 83 | 4    | D83D DE03    | 4    |
  | **合計** | **8バイト**    |      | **8バイト**     |      |

  ---

  ## 💡 ざっくり使い分け

  * **UTF-8**：Webやファイル保存、通信など → デファクト標準（世界中で主流）
  * **UTF-16**：Windows内部、C#、Javaの文字列 → 内部表現で多い

  ---

  ## まとめ

  つまり1文字を何byteで表すかの設定ということみたいです。
  utf-8の世界ではchar型が基本1byteになり、utf-16の世界ではchar型が基本2byteになるみたいですね。
  ただ一部例外は存在しているみたいで、絵文字などを表現する際はutf-16でも4byteになるそうです。これを考慮できていないと絵文字の`.Length`が2倍になって出てくることもあるのだとか…。

</details>

### T4テンプレート
各文字コードのディレクトリ内にはT4テンプレートである`.tt`ファイルが用意されており、テンプレートを使ってクラスの実装が可能になっています。これは後程詳しく扱うのですが、ZStringの関数にはほぼ同じ処理を異なる型に対して行うオーバーロード関数が沢山用意されています。
他にも引数の数が1個から16個までのバージョンを用意していたりするため、実装の楽のために用意されたのだと予想できます。（引数の数や型が違うだけの関数を沢山実装するのは苦痛なだけですからね…）

それではディレクトリ構造をざっと確認したところで早速各ファイルの実装を見ていきましょう。

## ZString.cs

まずはこのライブラリの名前を関するZString.csからです。名前の通りこのライブラリを使う際の窓口となるZStringクラスが定義されています。
このファイルは中身が短いので全文を出したいと思います。

```cs
namespace Cysharp.Text
{
    public static partial class ZString
    {
        public static Utf16ValueStringBuilder CreateStringBuilder()
        {
            var builder = new Utf16ValueStringBuilder();
            builder.Init();
            return builder;
        }

        public static Utf8ValueStringBuilder CreateUtf8StringBuilder()
        {
            var builder = new Utf8ValueStringBuilder();
            builder.Init();
            return builder;
        }
    }
}
```

非常に単純ですね。
定義されているのは2関数のみで、各文字コードに対応するStringBuilderクラスを取得する関数だけです。
一応見るべきところがあるとすれば関数名でしょうか。utf-16は単に`CreateStringBuilder()`なのに対してutf-8は`CreateUtf8StringBuilder()`となっています。ZString的なデフォルトはutf-16ということなのでしょう。
実際.NETの[ドキュメント](https://learn.microsoft.com/ja-jp/dotnet/standard/base-types/character-encoding-introduction)を確認すると、string型やchar型は内部的に16bitを使用しているようです。C#的にもutf-16が標準ということなので、この関数名は妥当なのでしょう。特殊な事情が無い限りは文字コードを意識してプログラミングしたくはないですからね。

この実装から実際の`Format()`関数などは`Utf16ValuesStringBuilder`と`Utf8ValuesStringBuilder`に実装されているようです。
さて早速見ていきましょう...と言いたいところですが、実装のカロリーが高そうだったため今回の記事はここまでとしたいと思います。詳しい実装は次回の記事で見ていきます。
それでは次回に。
