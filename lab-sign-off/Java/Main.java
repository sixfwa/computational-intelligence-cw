import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

class Main {

    public static void main(String[] args) {
        AntennaArray antennaArray = new AntennaArray(5, 15);

        double[] design = particleSwarmOptimisation(antennaArray, 10);
        displayDesign(design);
        System.out.println(antennaArray.evaluate(design));

    }

    private static void displayDesign(double[] design) {
        for (double elem : design) {
            System.out.print(elem + ", ");
        }
    }

    private static double[] particleSwarmOptimisation(AntennaArray antennaArray, int iterations) {
        Particle[] swarm = new Particle[20];
        for (int i = 0; i < swarm.length; i++) {
            swarm[i] = new Particle(antennaArray);
        }
        for (int i = 0; i < iterations; i++) {
            for (Particle particle : swarm) {
                particle.step(antennaArray, 0.7211, 1.1193, 1.1193);
            }
        }
        return Particle.getGlobalBestPosition();
    }

    public static double[] randomSearch(AntennaArray antennaArray, int iterations) {
        double[] bestDesign = generateRandomValidDesign(antennaArray);
        double bestCost = antennaArray.evaluate(bestDesign);
        for (int i = 0; i < iterations; i++) {
            double[] newDesign = generateRandomValidDesign(antennaArray);
            double newCost = antennaArray.evaluate(newDesign);
            if (newCost < bestCost) {
                bestDesign = newDesign;
                bestCost = newCost;
            }
        }

        return bestDesign;
    }

    public static double[] generateRandomValidDesign(AntennaArray antennaArray) {
        int length = antennaArray.getNumberOfAntennae();
        double lowerBound = antennaArray.bounds()[0][0];
        double upperBound = antennaArray.bounds()[1][1];
        double[] design = new double[length];
        while (true) {
            for (int i = 0; i < antennaArray.getNumberOfAntennae() - 1; i++) {
                design[i] = ThreadLocalRandom.current().nextDouble(lowerBound, upperBound);
            }
            design[antennaArray.getNumberOfAntennae() - 1] = upperBound;
            Arrays.sort(design);
            if (antennaArray.is_valid(design)) {
                break;
            }
        }
        return design;
    }
}