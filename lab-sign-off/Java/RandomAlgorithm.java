import java.util.Random;
import java.util.Arrays;

class RandomAlgorithm {

    private AntennaArray antennaArray;

    public RandomAlgorithm(AntennaArray antennaArray) {
        this.antennaArray = antennaArray;
    }

    public double[] generateRandomValidDesign() {
        double[] design = new double[3];
        Random r = new Random();
        while (true) {
            double min_one = antennaArray.bounds()[1][0];
            double max_one = min_one + antennaArray.MIN_SPACING;
            design[0] = min_one + (max_one - min_one) * r.nextDouble();
            double min_two = antennaArray.MIN_SPACING;
            double max_two = antennaArray.bounds()[1][1] - antennaArray.MIN_SPACING;
            design[1] = min_two + (max_two - min_two) * r.nextDouble();
            design[2] = antennaArray.bounds()[1][1];
            Arrays.sort(design);
            if (antennaArray.is_valid(design))
                break;
        }

        return design;
    }

    public double[] randomSearch(int iterations) {
        double[] bestDesign = generateRandomValidDesign();
        double bestCost = antennaArray.evaluate(bestDesign);
        for (int i = 0; i < iterations; i++) {
            double[] newDesign = generateRandomValidDesign();
            double newCost = antennaArray.evaluate(newDesign);
            if (newCost < bestCost) {
                bestDesign = newDesign;
                bestCost = newCost;
            }
        }

        return bestDesign;
    }
}