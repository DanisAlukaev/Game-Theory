package gametheory.assignment2.your_strategy;
import gametheory.assignment2.Player;
import java.util.*;


public class Strat implements Player {
    private final ArrayList<Integer> acceptableMoves;
    private Boolean isSegmented;
    private Boolean isAggressive;
    private int restingField;
    private int opponentField;
    private int myField;
    private int patience;
    private int myLastMove;

    

    public Strat() {
        acceptableMoves = new ArrayList<>(Arrays.asList(1, 2, 3));
        initialize();
    }

    private void initialize() {
        isSegmented = false;
        isAggressive = false;
        restingField = -1;
        opponentField = -1;
        myField = -1;
        patience = 1;
        myLastMove = -1;
    }

    @Override
    public void reset() {
        initialize();
    }

    private int random_move() {
        int choice = 1 + (int) (Math.random() * 3);
        myLastMove = choice;
        return choice;
    }

    private int greedy_move(int xA, int xB, int xC) {
        final ArrayList<Integer> numbers = new ArrayList<>(Arrays.asList(xA, xB, xC));
        final int maxElement = Collections.max(numbers);
        final ArrayList<Integer> maxElements = new ArrayList<>(3);
        for (int i = 0; i < numbers.size(); i++) {
            if (numbers.get(i).equals(maxElement)) {
                maxElements.add(i + 1);
            }
        }
        int choice = maxElements.get(new Random().nextInt(maxElements.size()));
        myLastMove = choice;
        return choice;
    }

    @Override
    public int move(int opponentLastMove, int xA, int xB, int xC) {

        if (!isSegmented) {
            // Players have not chosen their fields yet.
            if (myLastMove == -1) {
                // Take zero step at random.
                int myResidence = random_move();
                return myResidence;
            } else {
                // Check if opponent selected different field.
                if (myLastMove == opponentLastMove) {
                    int myResidence = random_move();
                    return myResidence;
                }
                // Assume that fields are distributed.
                isSegmented = true;
                myField = myLastMove;
                opponentField = opponentLastMove;
                restingField = 6 - myLastMove - opponentLastMove;
            }
        } 
        // Players have chosen their fields.

        // Check if opponent broke the rules.
        if (opponentLastMove == myField) {
            isAggressive = true;
        }
        System.out.println(" ");
        // Make a move.
        final ArrayList<Integer> vegetation = new ArrayList<>(Arrays.asList(xA, xB, xC));
        if (!isAggressive) {
            // Agent stick to live and let live strategy.
            if (vegetation.get(myField - 1) > 4) {
                myLastMove = myField;
                return myField;
            } else {
                myLastMove = restingField;
                return restingField;
            }
        } else {
            // Agent become greedy.
            return greedy_move(xA, xB, xC);
        }
    }

    @Override
    public String getEmail() {
        return "d.alukaev@innopolis.university";
    }
}