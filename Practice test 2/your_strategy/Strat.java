package gametheory.assignment2.your_strategy;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import gametheory.assignment2.Player;


public class Strat implements Player {

    @Override
    public void reset() {
        // kek
    }

    @Override
    public int move(int opponentLastMove, int xA, int xB, int xC) {
        ArrayList<Integer> numbers = new ArrayList<>(Arrays.asList(xA, xB, xC));
        int choice = 1 + numbers.indexOf(Collections.max(numbers));
        return choice;
    }

    @Override
    public String getEmail() {
        return "d.alukaev@innopolis.university";
    }
}