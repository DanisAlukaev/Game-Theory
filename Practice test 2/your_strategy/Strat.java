package gametheory.assignment2.your_strategy;
import gametheory.assignment2.Player;
import java.util.*;


public class Strat implements Player {

    private final ArrayList<Integer> moves;

    public Strat() {
        moves = new ArrayList<>();
    }

    @Override
    public void reset() {
        moves.clear();
    }

    @Override
    public int move(int opponentLastMove, int xA, int xB, int xC) {
        final ArrayList<Integer> numbers = new ArrayList<>(Arrays.asList(xA, xB, xC));
        final int maxElement = Collections.max(numbers);
        final ArrayList<Integer> maxElements = new ArrayList<>(3);
        for (int i = 0; i < numbers.size(); i++) {
            if (numbers.get(i).equals(maxElement)) {
                maxElements.add(i + 1);
            }
        }
        int choice = maxElements.get(new Random().nextInt(maxElements.size()));
        moves.add(choice);
        return choice;
    }

    @Override
    public String getEmail() {
        return "d.alukaev@innopolis.university";
    }
}