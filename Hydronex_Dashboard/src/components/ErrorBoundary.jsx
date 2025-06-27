import React from "react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Met à jour l'état pour afficher le fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Tu peux loguer l'erreur vers un service externe ici
    this.setState({ errorInfo });
    console.error("Erreur capturée par ErrorBoundary:", error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    // Tu peux aussi appeler une prop reset si tu veux faire plus
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-6 bg-red-100 rounded-lg text-red-800">
          <h2 className="text-xl font-bold mb-2">Une erreur est survenue.</h2>
          <details style={{ whiteSpace: "pre-wrap" }}>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo?.componentStack}
          </details>
          <button
            onClick={this.handleReset}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Réessayer
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
