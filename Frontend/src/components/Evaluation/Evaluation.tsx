import style from "./Evaluation.module.scss";

export default function Evaluation
    (props: { bgColor: string, dotColor: string, cntDot: number, text: string }) {
    return <div className={style.background} style={{ backgroundColor: props.bgColor }}>
        {props.text}:
        <div className={style.dotContainer}>
            {Array(10).fill(0).map((_, index) => (
                <Dot color={index < props.cntDot ? props.dotColor : 'white'} />
            ))}
        </div>
    </div>
}

function Dot(props: { color: string }) {
    return <div className={style.dot} style={{ backgroundColor: props.color }} />
}