<?php

$base64 = $_POST['base64'];
if (preg_match('/^(data:\s*image\/(\w+);base64,)/', $base64, $result)) {
    $type = $result[2];
    $img = "../image/" . iconv('utf-8', 'gb2312//IGNORE', $_POST['location']) . date('md', time()) . ".{$type}";
    if (file_put_contents($img, base64_decode(str_replace($result[1], '', $base64)))) {
        echo '新文件保存成功：', $img;
    } else {
        echo '新文件保存失败';
    }
}
