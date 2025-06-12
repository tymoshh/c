<?php
session_start();
header('Content-Type: application/json');

// Inicjalizacja balansu
if (!isset($_SESSION['balance'])) {
    $_SESSION['balance'] = 1000;
}

$balance = $_SESSION['balance'];
$cost = 50;

if ($balance < $cost) {
    echo json_encode([
        "result" => [1, 1],
        "sum" => 2,
        "message" => "Brak środków!",
        "win" => 0,
        "balance" => $balance
    ]);
    exit;
}

// Odejmij koszt gry
$balance -= $cost;

// Losowanie 2 kości
$dice1 = rand(1, 6);
$dice2 = rand(1, 6);
$sum = $dice1 + $dice2;
$win = 0;
$message = "";

if ($sum >= 2 && $sum <= 6) {
    $win = 50; // np. 2x stawki
    $message = "🎉 Wygrałeś (nisko)!";
} elseif ($sum >= 8 && $sum <= 12) {
    $win = 75;
    $message = "🎉 Wygrałeś (wysoko)!";
} else {
    $message = "💀 Przegrałeś (suma = 7)";
}

$balance += $win;
$_SESSION['balance'] = $balance;

echo json_encode([
    "result" => [$dice1, $dice2],
    "sum" => $sum,
    "message" => $message,
    "win" => $win,
    "balance" => $balance
]);
