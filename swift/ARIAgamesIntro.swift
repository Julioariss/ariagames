import SwiftUI

/// Intro de marca ARIAgames para el arranque de cada juego (watchOS/iOS).
/// Uso: ARIAgamesIntro { mostrarMenu = true }
struct ARIAgamesIntro: View {
    var onFinish: () -> Void

    private let red = Color(red: 0.90, green: 0.035, blue: 0.08)
    private let ink = Color(red: 0.04, green: 0.04, blue: 0.04)
    private let paper = Color(red: 0.965, green: 0.957, blue: 0.94)

    @State private var lineW: CGFloat = 0
    @State private var curtain = false
    @State private var letters = [false, false, false, false]
    @State private var ring = false
    @State private var gamesIn = false
    @State private var bar = false
    @State private var shine = false
    @State private var shake = false
    @State private var fade = false

    var body: some View {
        GeometryReader { g in
            let w = g.size.width, h = g.size.height
            let fs = w * 0.30
            ZStack {
                paper.ignoresSafeArea()

                // shockwave
                Circle().stroke(red, lineWidth: 2)
                    .frame(width: 10, height: 10)
                    .scaleEffect(ring ? 40 : 0.1)
                    .opacity(ring ? 0 : 0.9)

                VStack(spacing: 2) {
                    HStack(spacing: 0) {
                        ForEach(0..<4, id: \.self) { i in
                            Text(String(Array("ARIA")[i]))
                                .font(.system(size: fs, weight: .black).italic())
                                .foregroundStyle(red)
                                .offset(y: letters[i] ? 0 : -h * 1.3)
                                .scaleEffect(y: letters[i] ? 1 : 1.6)
                                .opacity(letters[i] ? 1 : 0)
                        }
                    }
                    Text("games")
                        .font(.system(size: fs * 0.82, weight: .bold))
                        .foregroundStyle(ink)
                        .offset(x: gamesIn ? 0 : w * 0.8)
                        .blur(radius: gamesIn ? 0 : 12)
                        .opacity(gamesIn ? 1 : 0)
                    Rectangle().fill(ink)
                        .frame(width: bar ? w * 0.7 : 0, height: 3)
                        .overlay(alignment: .trailing) { Rectangle().fill(red).frame(width: w * 0.12) }
                        .frame(maxWidth: .infinity, alignment: .center)
                }
                .offset(x: shake ? 3 : 0)
                .overlay {
                    LinearGradient(colors: [.clear, .white.opacity(0.9), .clear], startPoint: .leading, endPoint: .trailing)
                        .frame(width: w * 0.4)
                        .offset(x: shine ? w : -w)
                        .blendMode(.overlay)
                        .allowsHitTesting(false)
                }

                // curtains + red line
                VStack(spacing: 0) {
                    ink.frame(height: curtain ? 0 : h / 2)
                    Spacer(minLength: 0)
                    ink.frame(height: curtain ? 0 : h / 2)
                }.ignoresSafeArea()
                Rectangle().fill(red).frame(width: lineW, height: 2)
                    .shadow(color: red, radius: 8)
                    .opacity(curtain ? 0 : 1)
            }
            .opacity(fade ? 0 : 1)
            .task { await run(w: w) }
        }
    }

    private func run(w: CGFloat) async {
        withAnimation(.easeOut(duration: 0.5)) { lineW = w }
        try? await Task.sleep(for: .seconds(0.55))
        withAnimation(.easeInOut(duration: 0.6)) { curtain = true }
        try? await Task.sleep(for: .seconds(0.4))
        for i in 0..<4 {
            withAnimation(.interpolatingSpring(stiffness: 220, damping: 11)) { letters[i] = true }
            try? await Task.sleep(for: .seconds(0.1))
        }
        withAnimation(.easeOut(duration: 0.9)) { ring = true }
        withAnimation(.easeOut(duration: 0.1).repeatCount(4)) { shake = true }
        try? await Task.sleep(for: .seconds(0.4))
        withAnimation(.spring(response: 0.7, dampingFraction: 0.82)) { gamesIn = true }
        try? await Task.sleep(for: .seconds(0.6))
        withAnimation(.easeOut(duration: 0.6)) { bar = true }
        withAnimation(.easeInOut(duration: 0.9)) { shine = true }
        try? await Task.sleep(for: .seconds(1.6))
        withAnimation(.easeIn(duration: 0.4)) { fade = true }
        try? await Task.sleep(for: .seconds(0.4))
        onFinish()
    }
}

#Preview { ARIAgamesIntro {} }
