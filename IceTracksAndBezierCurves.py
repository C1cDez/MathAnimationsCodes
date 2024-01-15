from manim import *
import math
import numpy as np


def lerp1(s: float, f: float, t: float) -> float:
    return s + (f - s) * t

def lerpDot(S: Dot, F: Dot, t: float) -> np.array:
    return np.array([
        lerp1(S.get_x(), F.get_x(), t),
        lerp1(S.get_y(), F.get_y(), t),
        0
    ])

def normilizeVec(v: np.array) -> np.array:
    return v / (math.sqrt(v[0] * v[0] + v[1] * v[1]))


strLerpFormula = r"\operatorname{lerp} \left(s,f,t\right)=s+\left(f-s\right)t"


def calculateQs(points: [Dot], Q0: Dot) -> [Dot]:
    qs: [Dot] = []
    qs.append(Q0)
    for k in range(1, len(points)):
        p = points[k]
        qs.append(calculateQ_(p, qs[k - 1]))
    return qs


def calculateQ_(p: Dot, q_k1: Dot) -> Dot:
    return Dot([2 * p.get_x() - q_k1.get_x(), 2 * p.get_y() - q_k1.get_y(), 0])


dots = [
    Dot([4, -2.5, 0]),
    Dot([2, 0, 0]),
    Dot([1, 2, 0]),
    Dot([0, 0.5, 0]),
    Dot([-4, 1, 0]),
    Dot([-2, -1, 0]),
    Dot([-3, -2, 0])
]
qDots = calculateQs(dots, Dot([2, -2, 0]))


def LERP2_Dots(Pk: Dot, Qk: Dot, Pk_1: Dot, t: float) -> np.array:
    return np.array([
        (Pk_1.get_x() - 2 * Qk.get_x() + Pk.get_x()) * t * t + 2 * (Qk.get_x() - Pk.get_x()) * t + Pk.get_x(),
        (Pk_1.get_y() - 2 * Qk.get_y() + Pk.get_y()) * t * t + 2 * (Qk.get_y() - Pk.get_y()) * t + Pk.get_y(),
        0
    ])

def LERP2_Dots_vel(Pk: Dot, Qk: Dot, Pk_1: Dot, t: float) -> np.array:
    return np.array([
        2 * (Pk_1.get_x() - 2 * Qk.get_x() + Pk.get_x()) * t + 2 * (Qk.get_x() - Pk.get_x()),
        2 * (Pk_1.get_y() - 2 * Qk.get_y() + Pk.get_y()) * t + 2 * (Qk.get_y() - Pk.get_y()),
        0
    ])


def parametricLERP_Dots_Curve(k: int) -> ParametricFunction:
    return ParametricFunction(lambda t: LERP2_Dots(dots[k], qDots[k], dots[k + 1], t), t_range=np.array([0, 1]), color=YELLOW)


def parametricLERP2_Dots_Curve(Pk: Dot, Qk: Dot, Pk_1: Dot) -> ParametricFunction:
    return ParametricFunction(lambda t: LERP2_Dots(Pk, Qk, Pk_1, t), t_range=np.array([0, 1]), color=YELLOW)


class MainScene(Scene):
    def construct(this):
        this.animation11()
        pass

    # First curve explanation
    def animation1(this):
        dotsSpeakingTime = 1.25
        curveSpeakingTime = 2
        nodesSpeakingTime = 1

        curvesBuffer = [ParametricFunction]


        for dot in dots:
            this.play(Create(dot), run_time=dotsSpeakingTime / len(dots))

        for k in range(len(qDots) - 1):
            parcurve = parametricLERP2_Dots_Curve(k)
            curvesBuffer.append(parcurve)
            this.play(Create(parcurve), run_time=curveSpeakingTime / (len(qDots) - 1))

        this.wait(1)

        this.play(Flash(dots[0], color=RED), run_time=0.5)
        this.play(Flash(dots[len(dots) - 1], color=RED), run_time=0.5)

        for di in range(1, len(dots) - 1):
            dot = dots[di]
            this.play(Flash(dot, color=RED), run_time=nodesSpeakingTime / (len(dots) - 2))

        this.wait(2)

        trackFormula = MathTex(r"P\left(t\right)=\left(x\left(t\right);y\left(t\right)\right)")
        trackFormula.move_to(4 * RIGHT + 3 * UP)
        this.play(Write(trackFormula), run_time=0.5)

        this.wait(3)

        for dot in dots:
            this.play(FadeOut(dot, shift=DOWN), run_time=0.15)
        for curve in curvesBuffer:
            this.remove(curve)
        this.play(FadeOut(trackFormula, shift=DOWN), run_time=0.15)

        pass

    #Partical Curve Explanation and Minecraft Interpritation
    def animation2(this):
        beforeFunctionSpeakingTime = 1.25
        beforeParameterSpeakingTime = 0.5
        aboutParameterSpeakingTime = 0.75
        beforeRemovingTilesSpeakingTime = 0.3
        beforeMinecraftSpeakingTime = 1
        loopSpeakingTime = 4

        Pk = Dot([1, -2, 0])
        Pk_1 = Dot([-4, 2, 0])

        Pk_title = MathTex(r"P_{k}")
        Pk_1_title = MathTex(r"P_{k+1}")

        Pk_title.next_to(Pk)
        Pk_1_title.next_to(Pk_1)

        Qk = Dot([-3, -1, 0])

        curve = parametricLERP2_Dots_Curve(Pk, Qk, Pk_1)
        this.play(Create(curve), run_time=1.5)

        this.play(Create(Pk), run_time=0.3)
        this.play(Write(Pk_title), run_time=0.1)
        this.play(Create(Pk_1), run_time=0.3)
        this.play(Write(Pk_1_title), run_time=0.1)

        this.wait(beforeFunctionSpeakingTime)

        LFunction = MathTex(r"L_{k}\left(t\right)")
        LFunction.move_to(LEFT * 1.75)
        LFunction.rotate(-PI / 6)
        this.play(Write(LFunction), run_time=0.5)

        this.wait(beforeParameterSpeakingTime)


        paramTIn = MathTex(r"t \in [0;1]")
        paramTIn.move_to(DOWN * 3 + RIGHT * 5)
        this.play(Write(paramTIn), run_time=0.5)
        this.wait(aboutParameterSpeakingTime)
        this.play(Wiggle(paramTIn), run_time=0.5)

        this.play(FadeOut(LFunction, shift=DOWN), run_time=0.2)
        this.play(FadeOut(paramTIn, shift=DOWN), run_time=0.2)

        tInitialPos = LERP2_Dots(Pk, Qk, Pk_1, 0)
        tLabel = Variable(var=0, label="t")
        tLabel.move_to(tInitialPos + UP * 0.5 + RIGHT * 0.5)
        this.play(Write(tLabel), run_time=0.1)
        destTDot = Dot(tInitialPos, color=RED)
        LFunction_ = MathTex(r"L_{k}\left(t\right)")
        LFunction_.move_to(tInitialPos + DOWN * 0.5 + LEFT * 0.5)
        this.play(Create(destTDot), run_time=0.1)
        this.play(Create(LFunction_), run_time=0.1)
        tTracker = tLabel.tracker
        destTDot.add_updater(lambda x: (
            destTDot.move_to(LERP2_Dots(Pk, Qk, Pk_1, tTracker.get_value()))
        ))
        LFunction_.add_updater(lambda x: (
            LFunction_.move_to(LERP2_Dots(Pk, Qk, Pk_1, tTracker.get_value()) + DOWN * 0.5 + LEFT * 0.5)
        ))
        tLabel.add_updater(lambda x: (
            tLabel.move_to(LERP2_Dots(Pk, Qk, Pk_1, tTracker.get_value()) + UP * (1 - min(tTracker.get_value(), 0.5)) + RIGHT * min(tTracker.get_value(), 0.5) * 2)
        ))
        this.play(tTracker.animate.set_value(1), run_time=2)


        this.wait(beforeRemovingTilesSpeakingTime)
        this.play(FadeOut(tLabel, shift=UP), run_time=0.25)
        this.play(FadeOut(LFunction_, shift=UP), run_time=0.25)
        this.play(FadeOut(destTDot), run_time=0.25)
        this.wait(beforeMinecraftSpeakingTime)

        N_discreteDots: int = 20
        discreteDeltaT: float = 1 / N_discreteDots
        deltaT = MathTex(r"\Delta t=" + str(discreteDeltaT))
        deltaT.move_to(RIGHT * 3 + UP)
        this.play(Write(deltaT), run_time=0.5)
        nthDotFormula = MathTex(r"C_{n}=L_{k}\left(n\Delta t\right)")
        nthDotFormula.next_to(deltaT, DOWN * 3)
        this.play(Write(nthDotFormula), run_time=0.5)

        destNDots = [Dot]

        for n in range(N_discreteDots):
            nVar = MathTex(r"n=" + str(n))
            nVar.next_to(deltaT, DOWN)
            value = discreteDeltaT * n
            dot = Dot(LERP2_Dots(Pk, Qk, Pk_1, value), color=GREEN)
            CNDotInfo = MathTex(r"L_{k}\left(" + ("{:.2f}".format(value)) + r" \right)")
            CNDotInfo.next_to(dot, DOWN * 0.5 + LEFT * 0.5)

            destNDots.append(dot)

            this.add(nVar)
            this.play(Create(dot), run_time=loopSpeakingTime / N_discreteDots / 5)
            this.play(Create(CNDotInfo), run_time=loopSpeakingTime / N_discreteDots / 5)
            this.wait(loopSpeakingTime / N_discreteDots)
            this.play(FadeOut(CNDotInfo), run_time=loopSpeakingTime / N_discreteDots / 10)
            this.remove(nVar)


        this.wait(2)

        pass

    def animation3(this):
        formula = MathTex(strLerpFormula)
        this.play(Write(formula), run_time=0.5)
        rect = SurroundingRectangle(formula, buff=0.5)
        this.play(Create(rect), run_time=0.5)
        group = Group(formula, rect)
        this.play(Wiggle(group), run_time=1)
        this.play(FadeOut(rect), formula.animate.move_to(UP * 3), run_time=0.2)

        lerp = lambda s, f, t: s + (f - s) * t
        lerpDot = lambda S, F, t: Dot([lerp(S.get_x(), F.get_x(), t), lerp(S.get_y(), F.get_y(), t), 0])

        dot1 = Dot([3, 1, 0])
        dot2 = Dot([-3, -2, 0])
        line = Line(dot1, dot2, color=YELLOW)

        dot1Title = MathTex(r"S")
        dot2Title = MathTex(r"F")

        dot1Title.next_to(dot1)
        dot2Title.next_to(dot2, LEFT)

        this.play(Create(dot1), Create(dot1Title), Create(dot2), Create(dot2Title), Create(line), run_time=0.5)

        destDot = lerpDot(dot1, dot2, 0)
        destDot.set_color(RED)
        var = Variable(0, "t")
        var.next_to(destDot, RIGHT + DOWN * 0.75)
        tracker = var.tracker
        destDot.add_updater(lambda x: (
            destDot.move_to(lerpDot(dot1, dot2, tracker.get_value()))
        ))
        var.add_updater(lambda x: (
            var.next_to(destDot, RIGHT + DOWN * 0.75)
        ))
        this.play(Write(var), Create(destDot), run_time=0.25)
        this.play(tracker.animate.set_value(1), run_time=2)

        this.wait(2)
        pass

    def animation4(this):
        aboutDoubleInterpolationSpeakingTime = 1.5
        aboutResultInterpolationSpeakingTime = 1
        beforeCurveSpeakingTime = 1.5

        A, B, C = Dot([-2, -2.5, 0]), Dot([0, 2.5, 0]), Dot([3, -1.5, 0])
        A_title, B_title, C_title = MathTex(r"A"), MathTex(r"B"), MathTex(r"C")
        A_title.next_to(A, DOWN)
        B_title.next_to(B, UP)
        C_title.next_to(C, DOWN)
        this.play(Create(A), Create(B), Create(C), Write(A_title), Write(B_title), Write(C_title), run_time=0.5)

        this.wait(aboutDoubleInterpolationSpeakingTime)

        destT = 0.6
        D, E = Dot(lerpDot(A, B, destT)), Dot(lerpDot(B, C, destT))
        D_title, E_title = MathTex(r"D"), MathTex(r"E")
        D_title.next_to(D, LEFT)
        E_title.next_to(E)
        F = Dot(lerpDot(D, E, destT))
        F_title = MathTex(r"F")
        F_title.next_to(F, UP + LEFT * 0.5)

        lineAB = Line(A, B, color=YELLOW)
        lineBC = Line(B, C, color=YELLOW)
        lineDE = Line(D, E, color=YELLOW)

        this.play(Create(lineAB), run_time=0.25)
        this.play(TransformFromCopy(VGroup(A, B), D), TransformFromCopy(VGroup(A_title, B_title), D_title), run_time=0.5)
        this.play(Create(lineBC), run_time=0.25)
        this.play(TransformFromCopy(VGroup(B, C), E), TransformFromCopy(VGroup(B_title, C_title), E_title), run_time=0.5)

        this.wait(aboutResultInterpolationSpeakingTime)

        this.play(Create(lineDE), run_time=0.25)
        this.play(TransformFromCopy(VGroup(D, E), F), TransformFromCopy(VGroup(D_title, E_title), F_title), run_time=0.5)

        this.wait(beforeCurveSpeakingTime)

        this.play(FadeOut(D, D_title, E, E_title, F, F_title, lineDE), run_time=0.25)
        this.play(lineAB.animate.set_color(GREEN), lineBC.animate.set_color(GREEN), run_time=0.25)

        tCurveVar = Variable(0, "t")
        tCurveTracker = tCurveVar.tracker

        D_moving, E_moving = Dot(lerpDot(A, B, 0)), Dot(lerpDot(B, C, 0))
        D_moving_title, E_moving_title = MathTex(r"D"), MathTex(r"E")
        D_moving_title.next_to(D_moving, LEFT)
        E_moving_title.next_to(E_moving)

        D_moving.add_updater(lambda x: (
            D_moving.move_to(lerpDot(A, B, tCurveTracker.get_value()))
        ))
        E_moving.add_updater(lambda x: (
            E_moving.move_to(lerpDot(B, C, tCurveTracker.get_value()))
        ))
        D_moving_title.add_updater(lambda x: (
            D_moving_title.next_to(D_moving, LEFT)
        ))
        E_moving_title.add_updater(lambda x: (
            E_moving_title.next_to(E_moving)
        ))

        F_moving = Dot(lerpDot(D_moving, E_moving, 0))
        F_moving_title = MathTex(r"F")
        F_moving_title.next_to(F_moving)

        F_moving.add_updater(lambda x: (
            F_moving.move_to(lerpDot(D_moving, E_moving, tCurveTracker.get_value()))
        ))
        F_moving_title.add_updater(lambda x: (
            F_moving_title.next_to(F_moving)
        ))

        curve = ParametricFunction(lambda t: lerpDot(Dot(lerpDot(A, B, t)), Dot(lerpDot(B, C, t)), t), t_range=np.array([0, 1]), color=YELLOW)

        this.play(Create(D_moving), Create(E_moving), Write(D_moving_title), Write(E_moving_title),
                  Create(F_moving), Write(F_moving_title), run_time=0.25)

        this.play(tCurveTracker.animate.set_value(1), Create(curve), run_time=1.5)

        this.wait(4)
        pass

    def animation5(this):
        about2SpeakingTime = 2
        about3SpeakingTime = 3
        beforeDisadvantageSpeakingTime = 3

        A, B, C = Dot([-4, -2.5, 0]), Dot([-2, 2.5, 0]), Dot([1, -1.5, 0])
        A_title, B_title, C_title = MathTex(r"A"), MathTex(r"B"), MathTex(r"C")
        A_title.next_to(A, DOWN)
        B_title.next_to(B, UP)
        C_title.next_to(C, DOWN)
        this.play(Create(A), Create(B), Create(C), Write(A_title), Write(B_title), Write(C_title), run_time=0.25)

        curve2 = ParametricFunction(lambda t: lerpDot(Dot(lerpDot(A, B, t)), Dot(lerpDot(B, C, t)), t), t_range=np.array([0, 1]), color=YELLOW)
        this.play(Create(curve2), run_time=0.25)

        this.wait(about2SpeakingTime)

        D = Dot([2, 3, 0])
        D_title = MathTex(r"D")
        D_title.next_to(D, UP)

        this.play(Create(D), Write(D_title), run_time=0.5)

        curve3 = ParametricFunction(lambda t: lerpDot(Dot(lerpDot(Dot(lerpDot(A, B, t)), Dot(lerpDot(B, C, t), t), t)), Dot(lerpDot(Dot(lerpDot(B, C, t)), Dot(lerpDot(C, D, t), t), t)), t),
                                    t_range=np.array([0, 1]), color=YELLOW)
        this.play(ReplacementTransform(curve2, curve3), run_time=1.5)

        this.wait(about3SpeakingTime)

        E = Dot([4.5, 0, 0])
        E_title = MathTex(r"E")
        E_title.next_to(E, DOWN)

        this.play(Create(E), Write(E_title), run_time=0.5)

        curve4 = ParametricFunction(lambda t: lerpDot(Dot(lerpDot(Dot(lerpDot(Dot(lerpDot(A, B, t)), Dot(lerpDot(B, C, t)), t)), Dot(lerpDot(Dot(lerpDot(B, C, t)), Dot(lerpDot(C, D, t)), t)), t)), Dot(lerpDot(Dot(lerpDot(Dot(lerpDot(B, C, t)), Dot(lerpDot(C, D, t)), t)), Dot(lerpDot(Dot(lerpDot(C, D, t)), Dot(lerpDot(D, E, t)), t)), t)), t),
                                    t_range=np.array([0, 1]), color=YELLOW)
        this.play(ReplacementTransform(curve3, curve4), run_time=1.5)

        this.wait(beforeDisadvantageSpeakingTime)

        exclB, exclC, exclD = MathTex(r"!", color=RED), MathTex(r"!", color=RED), MathTex(r"!", color=RED)
        exclB.next_to(B)
        exclC.next_to(C)
        exclD.next_to(D)

        this.play(Flash(B, color=RED), run_time=0.4)
        this.play(Write(exclB),  run_time=0.1)
        this.play(Flash(C, color=RED), run_time=0.4)
        this.play(Write(exclC), run_time=0.1)
        this.play(Flash(D, color=RED), run_time=0.4)
        this.play(Write(exclD), run_time=0.1)

        this.play(Wiggle(exclB), Wiggle(exclC), Wiggle(exclD), run_time=1)

        this.wait(2)
        pass

    def animation6(this):
        Pk, Pk_1 = Dot([1, -2, 0]), Dot([-4, 2, 0])
        Pk_title, Pk_1_title = MathTex(r"P_{k}"), MathTex(r"P_{k+1}")
        Pk_title.next_to(Pk)
        Pk_1_title.next_to(Pk_1)

        Qk = Dot([-3, -1, 0])

        curve = ParametricFunction(lambda t: lerpDot(Dot(lerpDot(Pk, Qk, t)), Dot(lerpDot(Qk, Pk_1, t)), t), t_range=np.array([0, 1]), color=YELLOW)

        this.play(Create(Pk), Write(Pk_title), Create(Pk_1), Write(Pk_1_title), run_time=0.5)
        this.play(Create(curve), run_time=1)

        formulaEmpty = MathTex(r"L_{k}\left(t\right)")
        formulaEmpty.move_to(RIGHT * 2 + UP)

        this.play(Write(formulaEmpty), run_time=0.5)
        this.wait(0.5)

        formulaLerp = MathTex(r"L_{k}\left(t\right)=P_{k}+\left(P_{k+1}-P_{k}\right)t")
        formulaLerp.move_to(formulaEmpty)
        this.play(ReplacementTransform(formulaEmpty, formulaLerp), run_time=0.5)

        lerpCurve = ParametricFunction(lambda t: lerpDot(Pk, Pk_1, t), t_range=np.array([0, 1]), color=YELLOW)
        this.play(ReplacementTransform(curve, lerpCurve), run_time=0.5)

        this.wait(2)

        pass

    def animation7(this):
        dotNames = [MathTex]
        for i in range(len(dots)):
            dot = dots[i]
            dotName = MathTex(r"P_{" + str(i) + "}")
            dotName.next_to(dot, RIGHT)
            this.play(Create(dot), Write(dotName), run_time=0.1)
            dotNames.append(dotName)

        curves = [ParametricFunction]
        for i in range(len(dots) - 1):
            curve = ParametricFunction(lambda t: lerpDot(dots[i], dots[i + 1], t), t_range=np.array([0, 1]), color=YELLOW)
            this.play(Create(curve), run_time=0.1)
            curves.append(curve)

        this.wait(2)

        pass

    def animation8(this):
        beforeAddingQSpeakingTime = 1.5

        Pk, Pk_1 = Dot([1, -2, 0]), Dot([-4, 2, 0])
        Pk_title, Pk_1_title = MathTex(r"P_{k}"), MathTex(r"P_{k+1}")
        Pk_title.next_to(Pk)
        Pk_1_title.next_to(Pk_1)

        Qk = Dot([-3, -1, 0])
        Qk_title = MathTex(r"Q_{k}")
        Qk_title.next_to(Qk, LEFT)

        formulaLerp = MathTex(r"L_{k}\left(t\right)=P_{k}+\left(P_{k+1}-P_{k}\right)t")
        formulaLerp.move_to(RIGHT * 2 + UP)
        curveLerp = ParametricFunction(lambda t: lerpDot(Pk, Pk_1, t), t_range=np.array([0, 1]), color=YELLOW)

        formula = MathTex(
            r"L_{k}\left(t\right)=\left(P_{k+1}-2Q_{k}+P_{k}\right)t^{2}+ \\ 2\left(Q_{k}-P_{k}\right)t+P_{k}")
        formula.move_to(UP + RIGHT * 2)

        this.play(Create(Pk), Write(Pk_title), Create(Pk_1), Write(Pk_1_title), Create(curveLerp), Create(formulaLerp), run_time=0.5)

        this.wait(beforeAddingQSpeakingTime)

        this.play(Create(Qk), Write(Qk_title), run_time=0.5)
        curve = ParametricFunction(lambda t: lerpDot(Dot(lerpDot(Pk, Qk, t)), Dot(lerpDot(Qk, Pk_1, t)), t), t_range=np.array([0, 1]), color=YELLOW)
        this.play(ReplacementTransform(curveLerp, curve), ReplacementTransform(formulaLerp, formula), run_time=0.5)

        this.wait(2)

        pass

    def animation9(this):
        dotNames = [MathTex]
        for i in range(len(dots)):
            dot = dots[i]
            dotName = MathTex(r"P_{" + str(i) + "}")
            dotName.next_to(dot, RIGHT)
            this.play(Create(dot), Write(dotName), run_time=0.15)
            dotNames.append(dotName)

        qDotNames = [MathTex]
        for i in range(len(qDots)):
            qDot = qDots[i]
            qDot.set_color(GREEN)
            qDotName = MathTex(r"Q_{" + str(i) + "}", color=GREEN)
            qDotName.next_to(qDot, RIGHT)
            this.play(Create(qDot), Write(qDotName), run_time=0.15)
            qDotNames.append(qDotName)

        curves = [ParametricFunction]
        for i in range(len(dots) - 1):
            curve = ParametricFunction(lambda t: lerpDot(Dot(lerpDot(dots[i], qDots[i], t)), Dot(lerpDot(qDots[i], dots[i + 1], t)), t), t_range=np.array([0, 1]),
                                       color=YELLOW)
            this.play(Create(curve), run_time=0.15)
            curves.append(curve)

        this.wait(2)
        pass

    def animation10(this):
        Pk, Pk_1, Pk_2 = Dot([0, -2, 0]), Dot([-3, 2, 0]), Dot([-6, -1, 0])
        Pk_title, Pk_1_title, Pk_2_title = MathTex(r"P_{k}"), MathTex(r"P_{k+1}"), MathTex(r"P_{k+2}")
        Pk_title.next_to(Pk)
        Pk_1_title.next_to(Pk_1, UP)
        Pk_2_title.next_to(Pk_2)

        this.play(Create(Pk), Create(Pk_1), Create(Pk_2), Write(Pk_title), Write(Pk_1_title), Write(Pk_2_title), run_time=0.5)

        Qk, Qk_1 = Dot([-1, 1, 0]), Dot([-5, 3, 0])
        Qk_title, Qk_1_title = MathTex(r"Q_{k}"), MathTex(r"Q_{k+1}")
        Qk_title.next_to(Qk)
        Qk_1_title.next_to(Qk_1, LEFT)

        this.play(Create(Qk), Create(Qk_1), Write(Qk_title), Write(Qk_1_title), run_time=0.5)

        formula = MathTex(r"L_{k}\left(t\right)=\left(P_{k+1}-2Q_{k}+P_{k}\right)t^{2}+2\left(Q_{k}-P_{k}\right)t+P_{k}")
        formula.scale(0.75)
        formula.move_to(RIGHT * 2.75 + UP * 3)
        this.play(Write(formula), run_time=0.5)

        curve_k = ParametricFunction(lambda t: LERP2_Dots(Pk, Qk, Pk_1, t), t_range=np.array([0, 1]), color=YELLOW)
        curve_k_1 = ParametricFunction(lambda t: LERP2_Dots(Pk_1, Qk_1, Pk_2, t), t_range=np.array([0, 1]), color=YELLOW)

        this.play(Create(curve_k), run_time=0.25)
        this.play(Create(curve_k_1), run_time=0.25)

        this.play(FadeOut(curve_k, curve_k_1), run_time=0.5)
        this.remove(curve_k, curve_k_1)

        movingDot = Dot(LERP2_Dots(Pk, Qk, Pk_1, 0))
        tVar = Variable(0, "t")
        tTracker = tVar.tracker

        movingDot.add_updater(lambda x: (
            movingDot.move_to(LERP2_Dots(Pk, Qk, Pk_1, tTracker.get_value()))
        ))

        this.play(Create(movingDot), run_time=0.25)

        firstCurveMaxValue = 0.2
        curve_k_first = ParametricFunction(lambda t: LERP2_Dots(Pk, Qk, Pk_1, t), t_range=np.array([0, firstCurveMaxValue]), color=YELLOW)
        this.play(tTracker.animate.set_value(firstCurveMaxValue), Create(curve_k_first), run_time=1.5)

        velocityFormula = Tex(r"$v_{k}\left(t\right)=$ Velocity")
        velocityFormula.next_to(formula, DOWN * 1.5)
        this.play(Write(velocityFormula), run_time=0.5)

        velocityVectorArrow = Arrow(
            start=LERP2_Dots(Pk, Qk, Pk_1, tTracker.get_value()),
            end=LERP2_Dots(Pk, Qk, Pk_1, tTracker.get_value())+(LERP2_Dots_vel(Pk, Qk, Pk_1, tTracker.get_value()))*0.25,
            color=RED
        )
        velocityVectorArrow.add_updater(lambda x: (
            velocityVectorArrow.put_start_and_end_on(LERP2_Dots(Pk, Qk, Pk_1, tTracker.get_value()), LERP2_Dots(Pk, Qk, Pk_1, tTracker.get_value())+(LERP2_Dots_vel(Pk, Qk, Pk_1, tTracker.get_value()))*0.25)
        ))
        this.play(Create(velocityVectorArrow), run_time=0.5)

        secondCurveMaxValue = 1
        curve_k_second = ParametricFunction(lambda t: LERP2_Dots(Pk, Qk, Pk_1, t), t_range=np.array([firstCurveMaxValue, secondCurveMaxValue]), color=YELLOW)

        this.play(tTracker.animate.set_value(secondCurveMaxValue), Create(curve_k_second), run_time=4)

        velocitiesEquivFormula = MathTex(r"v_{k}\left(1\right)=v_{k+1}\left(0\right)")
        velocitiesEquivFormula.next_to(velocityFormula, DOWN * 3)
        this.play(Write(velocitiesEquivFormula), run_time=0.5)
        this.play(Wiggle(velocitiesEquivFormula), run_time=1)

        this.wait(2.5)

        realVelocityFormula = MathTex(r"v_{k}\left(t\right)=\frac{d}{dt}L_{k}\left(t\right)")
        realVelocityFormula.next_to(formula, DOWN * 1.25)
        this.play(ReplacementTransform(velocityFormula, realVelocityFormula), run_time=0.5)

        this.wait(2.5)

        qFormula = MathTex(r"Q_{k+1}=2P_{k+1}-Q_{k}")
        qFormula.move_to(RIGHT * 3.75 + DOWN)
        qFormula.scale(1.25)
        this.play(TransformFromCopy(VGroup(velocitiesEquivFormula, realVelocityFormula), qFormula), run_time=1)
        surRect = SurroundingRectangle(qFormula, buff=0.25)
        this.play(Create(surRect), run_time=0.5)
        this.play(Wiggle(qFormula), Wiggle(surRect), run_time=1)
        this.wait(0.75)
        this.play(FadeOut(surRect), run_time=0.25)

        this.wait(1)

        q0Problem = MathTex(r"Q_{0}=?")
        q0Problem.next_to(qFormula, DOWN * 2)
        this.play(Write(q0Problem), run_time=0.5)

        this.wait(2)

        pass

    def animation11(this):
        Pk, Pk_1, Pk_2 = Dot([2, -3, 0]), Dot([-1, 1, 0]), Dot([-4, -2, 0])
        Pk_title, Pk_1_title, Pk_2_title = MathTex(r"P_{k}"), MathTex(r"P_{k+1}"), MathTex(r"P_{k+2}")
        Pk_title.next_to(Pk)
        Pk_1_title.next_to(Pk_1, UP)
        Pk_2_title.next_to(Pk_2)

        this.play(Create(Pk), Create(Pk_1), Create(Pk_2), Write(Pk_title), Write(Pk_1_title), Write(Pk_2_title),
                  run_time=0.5)

        Qk, Qk_1 = Dot([1, 0, 0]), Dot([-3, 2, 0])
        Qk_title, Qk_1_title = MathTex(r"Q_{k}"), MathTex(r"Q_{k+1}")
        Qk_title.next_to(Qk)
        Qk_1_title.next_to(Qk_1, LEFT)

        this.play(Create(Qk), Create(Qk_1), Write(Qk_title), Write(Qk_1_title), run_time=0.5)

        curve_k = ParametricFunction(lambda t: LERP2_Dots(Pk, Qk, Pk_1, t), t_range=np.array([0, 1]), color=YELLOW)
        curve_k_1 = ParametricFunction(lambda t: LERP2_Dots(Pk_1, Qk_1, Pk_2, t), t_range=np.array([0, 1]),
                                       color=YELLOW)

        this.play(Create(curve_k), run_time=0.5)
        this.play(Create(curve_k_1), run_time=0.5)

        qFormula = MathTex(r"Q_{k+1}=2P_{k+1}-Q_{k}")
        qFormula.move_to(RIGHT * 4 + UP)
        formula = MathTex(r"P_{k+1}=\frac{Q_{k+1}+Q_{k}}{2}")
        formula.move_to(qFormula)

        this.play(Write(qFormula), run_time=0.5)
        this.wait(0.5)
        this.play(ReplacementTransform(qFormula, formula), run_time=0.75)

        this.wait(1)

        line = Line(start=Qk, end=Qk_1)
        this.play(Create(line), run_time=1.5)

        this.wait(1)

        this.play(FadeOut(curve_k, curve_k_1), run_time=0.5)

        coff: float = (Qk_1.get_y() - Qk.get_y()) / (Qk_1.get_x() - Qk.get_x())
        incoff: float = -1 / coff
        Mk = Dot(lerpDot(Qk, Pk_1, 0.5))
        Mk_1 = Dot(lerpDot(Pk_1, Qk_1, 0.5))
        mk, mk_1 = Mk.get_y() - incoff * Mk.get_x(), Mk_1.get_y() - incoff * Mk_1.get_x()
        dx = 0.05
        Mk_func, Mk_1_func = FunctionGraph(lambda x: incoff * x + mk, x_range=[Mk.get_x() - dx, Mk.get_x() + dx]), \
            FunctionGraph(lambda x: incoff * x + mk_1, x_range=[Mk_1.get_x() - dx, Mk_1.get_x() + dx])
        Mk_func.set_color(WHITE)
        Mk_1_func.set_color(WHITE)
        this.play(Create(Mk_func), Create(Mk_1_func), run_time=1)

        this.wait(4)

        pass

