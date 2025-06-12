<?php
session_start();

if (!isset($_SESSION['balance'])) {
    $_SESSION['balance'] = 1000;
}

$balance = $_SESSION['balance'];
$bet = isset($_GET['bet']) ? (int) $_GET['bet'] : 0;

$allowedBets = [10, 100, 200, 500, 1000, 2000, 5000];

if (!in_array($bet, $allowedBets)) {
    echo json_encode(["result" => "❌", "balance" => $balance, "message" => "Nieprawidłowa kwota zakładu"]);
    exit;
}

if ($balance < $bet) {
    echo json_encode(["result" => "❌", "balance" => $balance, "message" => "Za mało środków"]);
    exit;
}
$wheel = [
    "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0",     // 11x przegrana
    "x1.5", "x1.5", "x1.5", "x1.5", "x1.5", "x1.5", "x1.5",                         // 4x x1.5
    "x2", "x2", "x2", "x2",                                       // 3x x2
    "x2.5", "x2.5",                                           // 2x x2.5
    "x3", "x3",                                               // 2x x3
    "x5",                                                    // 1x x5
    "JACKPOT"                                                // 1x x10
];

$result = $wheel[array_rand($wheel)];
$win = 0;

if ($result !== "0") {
    if ($result === "JACKPOT") {
        $win = $bet * 10;
    } else {
        $multiplier = floatval(str_replace("x", "", $result));
        $win = intval($bet * $multiplier);
    }
    $balance += $win;
}else{
    $balance -= $bet;
}

$_SESSION['balance'] = $balance;

echo json_encode([
    "result" => $result,
    "balance" => $balance,
    "message" => $win > 0 ? "🎉 Wygrałeś {$win}$!" : "😵 Nic nie wygrałeś."
]);
?>
