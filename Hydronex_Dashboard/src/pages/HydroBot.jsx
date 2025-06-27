import { useState, useEffect, useRef } from "react";
import { Send, User } from "lucide-react";
import botLogo from "../assets/icons/hydrobot.png";
import { sendMessageToBot } from "../services/chatService";
import { fetchAlerts } from "../services/deviceService";
import ReactMarkdown from "react-markdown";

export default function HydroBotChat() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Bonjour, comment puis-je vous aider aujourd'hui ?" },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [alertPrompts, setAlertPrompts] = useState([]);
  const bottomRef = useRef(null);

  useEffect(() => {
    const loadPrompts = async () => {
      try {
        const alerts = await fetchAlerts(null, 1, 2); // Dernières alertes
        const prompts = alerts.map((alert) => {
          const device = alert.dispositif_id
            ? `dispositif ${alert.dispositif_id}`
            : "un dispositif";
          return `Pourquoi cette alerte : "${alert.alerte}" sur ${device} ?`;
        });
        setAlertPrompts(prompts);
      } catch (e) {
        console.error("Erreur lors du chargement des alertes :", e);
      }
    };
    loadPrompts();
  }, []);

  const handleSend = async (customText = null) => {
    const textToSend = customText ?? input;
    if (!textToSend.trim()) return;

    const userMessage = { from: "user", text: textToSend };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const botReplyText = await sendMessageToBot(textToSend);
      const cleaned = botReplyText.replace(/\n/g, "\n\n");
      const botReply = { from: "bot", text: cleaned };
      setMessages((prev) => [...prev, botReply]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          from: "bot",
          text:
            "❌ Une erreur est survenue lors de la communication avec le serveur.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-full w-full bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-[#003366] text-white font-semibold text-lg px-6 py-3 flex items-center gap-2">
        <img src={botLogo} alt="HydroBot" className="w-6 h-6" />
        HydroBot
      </div>

      {/* Chat body */}
      <div className="flex-1 px-6 py-4 space-y-4 overflow-y-auto bg-blue-50">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`w-full flex ${
              msg.from === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`flex items-start gap-2 max-w-[60%] ${
                msg.from === "user" ? "flex-row-reverse" : ""
              }`}
            >
              <div className="w-6 h-6 shrink-0 rounded-full mt-1 bg-blue-400 text-white flex items-center justify-center">
                {msg.from === "user" ? (
                  <User className="w-4 h-4" />
                ) : (
                  <img src={botLogo} alt="HydroBot" className="w-5 h-5" />
                )}
              </div>

              <div className="relative">
                <div
                  className={`px-4 py-2 rounded-lg text-sm ${
                    msg.from === "user"
                      ? "bg-blue-400 text-white rounded-br-none"
                      : "bg-white text-gray-800 shadow rounded-bl-none"
                  }`}
                >
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                </div>

                <div
                  className={`absolute top-2 w-0 h-0 border-t-8 border-b-8 ${
                    msg.from === "user"
                      ? "right-[-8px] border-l-8 border-l-blue-400 border-t-transparent border-b-transparent"
                      : "left-[-8px] border-r-8 border-r-white border-t-transparent border-b-transparent"
                  }`}
                />
              </div>
              <div ref={bottomRef} />
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-center gap-2 max-w-[60%]">
              <div className="w-6 h-6 bg-blue-400 rounded-full flex justify-center items-center mt-1">
                <img src={botLogo} alt="HydroBot" className="w-5 h-5" />
              </div>
              <div className="bg-white text-gray-600 shadow px-4 py-2 text-sm rounded-lg rounded-bl-none animate-pulse">
                HydroBot vous répond...
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Suggestions */}
      {alertPrompts.length > 0 && (
        <div className="px-4 pb-2 flex flex-wrap gap-2 border-t border-gray-200 bg-white">
          {alertPrompts.map((prompt, index) => (
            <button
              key={index}
              onClick={() => handleSend(prompt)}
              className="bg-blue-100 hover:bg-blue-200 text-blue-800 text-xs px-3 py-1 rounded-full transition-all"
            >
              {prompt}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="px-4 py-3 flex items-center bg-white">
        <input
          type="text"
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-300 text-sm"
          placeholder="Écrivez un message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          disabled={isLoading}
        />
        <button
          onClick={() => handleSend()}
          className="ml-2 bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-full disabled:opacity-50"
          disabled={isLoading}
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
