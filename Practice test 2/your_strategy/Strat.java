package gametheory.assignment2.your_strategy;

import gametheory.assignment2.Player;

public class Strat implements Player {

    @Override
    public void reset() {
        // kek
    }

    @Override
    public int move(int opponentLastMove, int xA, int xB, int xC) {
        int choice = 1 + (int) (Math.random() * 3);
        return choice;
    }

    @Override
    public String getEmail() {
        return "d.alukaev@innopolis.university";
    }
}