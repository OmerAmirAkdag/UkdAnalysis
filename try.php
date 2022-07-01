<!DOCTYPE html>
<html>
<body>

<?php
$txt = "PHP";
echo "I love $txt!";
function print_results($result, $tournament_count, $match_count, $opponents_dictionary, $name, $surname, $galibiyet, $maglubiyet, $beraberlik){
	echo strtoupper($name) . " " . strtoupper($surname);
    echo "******************************************************";
    echo "Oynanan turnuva sayısı: ";
    echo $tournament_count .".<br>";
    echo "Oynanan mac sayısı: " ;
    echo $match_count .".<br>";
    echo "Toplam galibiyet sayısı: ";
    echo $galibiyet .".<br>";
    echo "Toplam maglubiyet sayısı: ";
    echo $maglubiyet .".<br>";
    echo "Toplam beraberlik sayısı: ";
    echo $beraberlik .".<br>";
    $puan = $galibiyet*1 + $beraberlik*0.5;
    $kazanma_orani = $puan/$match_count*100;
    echo "Kazanma Yüzdesi: % ";
    echo $kazanma_orani .".<br>";
    echo "******************************************************";
    echo "En çok oynanan opponents: ";
    for ($x = 0; $x < count($result); $x++) {
      echo $result[i][0] . "Maç sayısı:" . $result[i][1] . " Skor: " . $opponents_dictionary[$result[i][0]] - ($result[i][1]-$opponents_dictionary[$result[i][0]]) .".<br>";
    }
}
    
function upper_i($name){
	$word = "i";
	if(strpos($name, $word) !== false){
    	$name = str_replace("i" , "İ", $name);
    } 
    $name = strtoupper($name);
    return $name;
}

$opponents_before_formatting = [];
$opponents = [];
$turnuvalar = [];
$index = 1;
$person = None;
$no_id = "Lisans TCK Eksik";
$no_id_count = 0;
$no_ukd = 0;
$score = 0;
$opponents_scores = [];
$total_win = 0;
$total_draw = 0;
$total_loss = 0;
?>

</body>
</html>
