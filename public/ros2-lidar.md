---
title: 【ROS2】rviz2でLiDARの情報を見る
tags:
  - Python
  - ロボット
  - ROS2
private: false
updated_at: '2025-10-19T23:54:48+09:00'
id: f37cacec810651f0d030
organization_url_name: null
slide: false
ignorePublish: false
---
どうもこんにちは、kutoです。
今回はrviz2を用い、ROS2環境で北陽電機製LiDARの情報を取得、表示する方法について解説していきます。
ROS2やrviz2に関しては既にインストール済みであることを前提に解説していくので、インストール済みでない場合は他の記事を参考にインストールしてみてください。

## 使用環境
* ROS2 humble
* ubuntu 22.04 LTS
* LiDAR 

## そもそもLiDARとは？
以下の記事より引用し説明とします。詳しくは元の記事を参照ください。
https://zenn.dev/array/books/5efdb438cf8be3/viewer/15a40b

Lidarとは、「Light Detection And Ranging」の頭文字を取ったもので、反射光による物体検知または測距を行う方式を指します。（Lidar Image Detectionとも表現されます）
Lidarにはパルス状の光を発光する素子とそれを受信する素子があり、多くは
発光から受光までの時間差を測るToF (Time of Flight)の手法を用いています。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3792653/3b0a74bf-0a3f-2f9a-e09e-71a5037c6d11.png)
Lidarのセンサ自体は360°を測定しませんが、高性能なLidarはターンテーブルなどが設置されており、これが高速で回転することで360°の二次元データを出力します。
縦方向の角度を出力するLidarもあります。縦方向は「ライン」とカウントされることがあります。（例 : VLP-16 → 16ライン）

## インストール
まずは北陽電機の公式が公開していurg_node2のインストールから始めます。
似たものにurg_nodeというnodeが公開されていますが、こちらはROSのコミュニティによって公開されているものとなります。非公式ですので今回は使用しません。
https://github.com/ros-drivers/urg_node
それではインストールを行っていきます。いつも通りalt+ctrl+tでターミナルを開き、ros2の起動を行いましょう。
```bash
source /opt/ros/humble/setup.bash
```

まずは事前準備としてrosdepのインストールを行います。既に入っている場合は以下のコマンドを実行する必要はありません。
```bash
sudo apt install python3-rosdep
sudo rosdep init
```
rosdepの導入が終わったら、基本的には以下のコマンドを打っていけば問題ありません。gitからリポジトリを取ってきてインストールが完了します。
```bash
cd [ROS2用のワークスペース名]/src/
git clone --recursive https://github.com/Hokuyo-aut/urg_node2.git
rosdep update
rosdep install -i --from-paths urg_node2
cd ../
colcon build --symlink-install --packages-select urg_node2 
```
これでインストールは完了です。

## LiDAR設定
![IMG_0933.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3792653/4cb9ca85-e4b0-5fb3-1529-7b7abfb6be9c.jpeg)
以下のようにPCとLiDARを接続したあと、今回はLANコネクタによる接続を行うため、Ethernetの設定を行います。
有線接続をした状態でUbuntuの右上にある以下のようなアイコンをクリックしてください。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3792653/86e12422-2ef7-e236-f8e4-783b19e12f70.png)
クリックすると以下のようなポップアップが出てくると思うので、有線の欄をクリックし有線設定の画面を開いてください。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3792653/2563acde-4a29-8a26-5f93-a36bb6203004.png)
以下のような画面が開かれると思います。有線が接続済みになっていることを確認したら右側の設定アイコンをクリックしてください。
![Ethernet_config.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3792653/926ecbab-f6e0-c0e1-9861-95943ef0dd6a.png)
IPv4の欄から手動設定を選択し、アドレスを設定してください。
今回は以下のように設定してみました。設定をしたら、適用を押して設定を完了させましょう。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3792653/7b40b0bb-e0ee-a0d2-ac58-b45ced0f20ff.png)
設定し終わったらターミナルを開き、
```bash
ping [設定したアドレス番号]
```
と打ってみてください。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3792653/e4d1071a-093e-4525-8388-3f391966e117.png)
こんな感じの出力が得られれば設定が完了しています。この出力が得られない場合はどこかで間違えているので、再度設定をし直してみましょう。
設定の完了が確認できたら、nodeを起動させる前に今回設定したアドレスをnodeに設定する必要があります。
以下のコマンドを入力しVScodeを起動させてください。
```bash
cd src
code urg_node2
```
urg_node2フォルダーがVScodeで開かれると思います。config/params_ether.yamlを開き、ip_addressを以下のように使用するLiDARのIPアドレスに変えましょう。
```yaml
ip_address : '192.168.10.237'
```

これで事前設定は完了です。

## node起動
以下のコマンドで起動の準備をします。
```bash
cd ../
source install/setup.bash
```
そして以下のコマンドを打ちます。
```bash
ros2 launch urg_node2 urg_node2.launch.py
```
これでLiDARから情報をPCが取得できます。
あとは新しく別のターミナルを起動させ、以下のコマンドでrviz2を起動させましょう。
```bash
source /opt/ros/humble/setup.bash
rviz2
```
起動したらFixedFrameをlaserに変更し、下のaddからLaserScanを選択して追加します。
これで以下のような画面になれば成功です。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3792653/6236452b-5775-bdea-0e0d-36659f44c017.png)
