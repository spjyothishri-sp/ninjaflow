import os
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from features import create_features


def train_model():
    print("=" * 60)
    print("NinjaFlow Random Forest Model Training")
    print("=" * 60)

    X, y, df = create_features()

    print(f"Training rows  : {len(X)}")
    print(f"Features       : {X.shape[1]}")
    print()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    print(f"Training set   : {len(X_train)} rows")
    print(f"Testing set    : {len(X_test)} rows")
    print()

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    print("Training Random Forest...")
    model.fit(X_train, y_train)

    print("Training completed!")
    print()

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)
    print(f"Mean Absolute Error (MAE): {mae:.2f} days")
    print(f"R² Score                 : {r2:.4f}")
    print()

    print("Feature Importance:")

    importance = sorted(
        zip(X.columns, model.feature_importances_),
        key=lambda x: x[1],
        reverse=True
    )

    for feature, value in importance:
        print(f"  {feature:<35} {value:.4f}")

    model_path = os.path.join(
        os.path.dirname(__file__),
        "model.pkl"
    )

    joblib.dump(model, model_path)

    print()
    print("=" * 60)
    print("MODEL SAVED")
    print("=" * 60)
    print(f"Location: {model_path}")
    print()
    print("NinjaFlow ML training completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    train_model()