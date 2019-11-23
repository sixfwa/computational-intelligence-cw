import java.lang.Math;

class Particle {

    private static double[] globalBestPosition;
    private static double globalBestValue;

    private double[] position;
    private double[] velocity;
    private double[] personalBestPosition;
    private double personalBestValue;

    private AntennaArray antennaArray;

    public Particle(AntennaArray antennaArray) {
        this.antennaArray = antennaArray;
        globalBestValue = Double.MAX_VALUE;
        // randomly generated to lie in the feasible region
        position = Main.generateRandomValidDesign(antennaArray);
        velocity = setInitialVelocity();
        personalBestPosition = position;
        personalBestValue = antennaArray.evaluate(personalBestPosition);

        evaluate(antennaArray);
    }

    public static double[] getGlobalBestPosition() {
        return globalBestPosition;
    }

    public double[] getPosition() {
        return position;
    }

    public double[] getPersonalBestPosition() {
        return personalBestPosition;
    }

    public static double getGlobalBestValue() {
        return globalBestValue;
    }

    public double getPersonalBestValue() {
        return personalBestValue;
    }

    private double[] setInitialVelocity() {
        double[] randomPosition = Main.generateRandomValidDesign(antennaArray);
        double[] initialVelocity = vectorDifference(position, randomPosition);
        return initialVelocity;
    }

    // vectorOne - vectorTwo
    private double[] vectorDifference(double[] vectorOne, double[] vectorTwo) {
        double[] differenceVector = new double[vectorOne.length];
        for (int i = 0; i < vectorOne.length - 1; i++) {
            differenceVector[i] = Math.abs(vectorOne[i] - vectorTwo[i]);
        }
        differenceVector[vectorOne.length - 1] = vectorOne[vectorOne.length - 1];

        return differenceVector;
    }

    private double[] multiplyVector(double[] vector, double multiplier) {
        double[] newVector = new double[vector.length];
        for (int i = 0; i < vector.length - 1; i++) {
            newVector[i] = vector[i] * multiplier;
        }
        newVector[vector.length - 1] = vector[vector.length - 1];
        return newVector;
    }

    private double[] multiplyVectors(double[] vectorOne, double[] vectorTwo) {
        double[] differenceVector = new double[vectorOne.length];
        for (int i = 0; i < vectorOne.length - 1; i++) {
            differenceVector[i] = vectorOne[i] * vectorTwo[i];
        }
        differenceVector[vectorOne.length - 1] = vectorOne[vectorOne.length - 1];

        return differenceVector;
    }

    private double[] addThreeVectors(double[] vectorOne, double[] vectorTwo, double[] vectorThree) {
        double[] vector = new double[vectorOne.length];
        for (int i = 0; i < vectorOne.length - 1; i++) {
            vector[i] = vectorOne[i] + vectorTwo[i] + vectorThree[i];
        }
        vector[vectorOne.length - 1] = vectorOne[vectorOne.length - 1];

        return vector;
    }

    private double[] addVectors(double[] vectorOne, double[] vectorTwo) {
        double[] vector = new double[vectorOne.length];
        for (int i = 0; i < vectorOne.length - 1; i++) {
            vector[i] = vectorOne[i] + vectorTwo[i];
        }
        vector[vectorOne.length - 1] = vectorOne[vectorOne.length - 1];

        return vector;
    }

    public void step(AntennaArray antennaArray, double inertiaCoefficient, double cognitiveCoefficient,
            double socialCoefficient) {
        // inertia * velocity
        double[] inertiaVector = multiplyVector(velocity, inertiaCoefficient);

        // cognitive coefficient * random vector * (personal best - current position)
        // (personal best - current position)
        double[] cognitiveDistance = vectorDifference(personalBestPosition, position);
        // random vector
        double[] randomOne = Main.generateRandomValidDesign(antennaArray);
        // cognitive coefficient * random vector
        double[] coefRandOne = multiplyVector(randomOne, cognitiveCoefficient);
        double[] cognitiveAttraction = multiplyVectors(cognitiveDistance, coefRandOne);

        // social coefficient * random vector * (global best - current position)
        // (personal best - current position)
        double[] socialDistance = vectorDifference(globalBestPosition, position);
        // random vector
        double[] randomTwo = Main.generateRandomValidDesign(antennaArray);
        // social coefficient * random vector
        double[] coefRandTwo = multiplyVector(randomTwo, socialCoefficient);
        double[] socialAttraction = multiplyVectors(socialDistance, coefRandTwo);

        velocity = addThreeVectors(inertiaVector, cognitiveAttraction, socialAttraction);
        position = addVectors(position, velocity);
        System.out.println(globalBestValue);
    }

    private void evaluate(AntennaArray antennaArray) {
        double currentValue = antennaArray.evaluate(position);
        if (globalBestPosition == null) {
            globalBestPosition = position;
            globalBestValue = currentValue;
        } else if (currentValue < personalBestValue) {
            personalBestPosition = position;
            personalBestValue = currentValue;
            if (currentValue < globalBestValue) {
                globalBestPosition = position;
                globalBestValue = currentValue;
            }
        }
    }

}