<html>
    <head>
        <meta charset="UTF-8" />
        <title>测试 </title>
    </head>
    <body>
<?php
ini_set("error_reporting","E_ALL & ~E_NOTICE");
$baseUrl="https://piston-meta.mojang.com/mc/game/version_manifest.json";
$baseData = json_decode(file_get_contents($baseUrl),true);
echo "最新正式版：  ".$baseData['latest']['release'];
echo "<hr />";
echo "最新快照版：  ".$baseData['latest']['snapshot'];
echo "<hr />";
echo "<table border=\"1\">";
foreach ($baseData["versions"] as $value)
{
    if($value["type"]=="release"){
        $down_value = json_decode(file_get_contents($value["url"]),true);
    //."    下载链接：";
//    echo $down_value["url"];

    $i++;
    ?>
  <tr>
    <th><?php echo "序号：".$i ?></th>
    <th><?php echo "版本：".$value["id"] ?></th>
    <th><?php echo "类型：".$value["type"] ?></th>
    <th><?php echo "SHA1：".$down_value["downloads"]["server"]["sha1"] ?></th>
    <th>下载链接：<a href="<?php echo $down_value["downloads"]["server"]["url"] ?>">点击下载</a></th>
    <th><?php echo "大小：". sprintf("%.2f", round((($down_value["downloads"]["server"]["size"])/1024)/1024,2)) . MB ?></th>
  </tr>
<?php 
}
}
?>
</table>
</body>
</html>
