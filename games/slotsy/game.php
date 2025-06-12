<?php
session_start();

header('Content-Type: application/json');
if (!isset($_SESSION['balance'])) {
    $_SESSION['balance'] = 1000;
}

$balance = $_SESSION['balance'];
$cost = 10;

if ($balance < $cost) {
    echo json_encode([
        'result' => ['❌', '❌', '❌'],
        'win' => 0,
        'balance' => $balance,
        'message' => 'Brak środków na zakręcenie'
    ]);
    exit;
}

$balance -= $cost;

$symbols = ["🍒", "🍋", "🍇", "🍉", "🔔", "⭐", "7️⃣"];
$payouts = [
    "🍒" => 200,
    "🍋" => 300,
    "🍇" => 400,
    "🍉" => 500,
    "🔔" => 750,
    "⭐" => 1000,
    "7️⃣" => 2000,
];

$result = [];
for ($i = 0; $i < 3; $i++) {
    $result[] = $symbols[array_rand($symbols)];
}

if ($result[0] === $result[1] && $result[1] === $result[2]) {
    $win = $payouts[$result[0]];
} else {
    $win = 0;
}

$balance += $win;
$_SESSION['balance'] = $balance;

echo json_encode([
    'result' => $result,
    'win' => $win,
    'balance' => $balance,
    'message' => $win > 0 ? "Gratulacje! Wygrałeś $win$!" : "Niestety, brak wygranej"
]);
