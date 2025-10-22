---
title: ZStringを読もう(3) Utf16ValuesStringBuilder
tags:
  - C#
  - OSS
private: false
updated_at: ''
id: null
organization_url_name: null
slide: false
ignorePublish: false
---

どうもKutoです。
ということで、ZStringを読もうの第3回です。
前回はinitial commit時点でのディレクトリ構造やZString.csの紹介をしましたが、今回は実際にゼロアロケーション構築の根幹をなしているUtf16ValuesStringBuilderの実装を読んでいきたいと思います。

## Utf16ValuesStringBuilder.cs

以下のように`Utf16ValuesStringBuilder`には`partial`修飾子が付されており、複数ファイルにその実装がまたがるようになっています。
これは前回ちらっと話題に出したT4テンプレートでコードを生成させやすいように設定しているのだと考えられます。

よってまずは一番根幹の実装が詰まっている`Utf16ValuesStringBuilder.cs`を確認していきます。

```cs
namespace Cysharp.Text
{
    public ref partial struct Utf16ValueStringBuilder
    {
```

さあ最初の4行です。namespaceと構造体を宣言しているだけのたった4行ではありますが、ここからもうゼロアロケーションへの取り組みが見て取れます。

### classではなくstruct

通常このようなUtility系を組むときはclassを用いると思いますが、structを用いているというのが大きな工夫ポイントです。
何故classではいけないのか。これを説明するにはclassとstructの違いをしっかりと認識していなければいけません。

**classとstructの違い**
この2つ、違いをよく分からずに使っている人も多いのでしょうか？

「structは値型でclassは参照型である」
structとclassの違いをC#erに聞いたとき、ここまでは多くの方が回答として出せると思います。実際にこれは正しいですし、これに全てが詰まっているでしょう。
しかしでは値型と参照型の違いは？ この疑問に対しては答えられるでしょうか。

**値型と参照型の違い**
ここら辺の知識は曖昧な人も多いのではないでしょうか。自分も正直曖昧でした。
自分が認識していた違いは以下のようなものです。

|          | class |           struct             |
| -------- | ----- | ---------------------------- |
| 初期値    | null | 各メンバ変数にデフォルト値が入る | 
| new演算子 | 必要 |            不要                |
| 継承     |  可能 |           不可能               |

まとめれば、「継承できるからclass使っておけば良いんでしょ？」これが私の元々の認識でした。
実際パフォーマンスをそこまで求めらない環境ではこの認識でも特に問題は生じない気がします。
しかし本ライブラリのようなパフォーマンスを強く求める場においては、この認識では全く足りません。それぞれに対しより根本的な実装内容を把握しなければいけないのです。

**メモリ領域の違い**
structとclass、つまり値型と参照型の違いの根本は使用されるメモリ領域の違いに行きつきます。
どういうことかなのか。詳しく見ていきましょう。

まずは単純なstructの方から見ていきます。
例として以下のようなstructを考えていきたいと思います。

```cs
public struct Human
{
  int age;
  float height;
  float weight;
}
```

このHuman構造体を以下のように宣言したときメモリがどのように確保されるのかを見ていきましょう。

```cs
Human human;
```

まずこのコードが実行されると
