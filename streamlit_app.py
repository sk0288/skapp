from io import BytesIO

import streamlit as st
from PIL import Image

from fes.const import EXAMPLE_IMAGE_DIR
from fes.face_annotate import get_image_face_hided_by_emoji
from fes.models import Emoji


def render() -> None:
    st.title("自動で顔にスタンプくん")



    # 画像のアップロード
    user_image_fp = st.file_uploader("顔にスタンプを追加したい画像をアップロードしてください", type=["png", "jpg", "bmp"])



    # サンプル
    image_paths = {
        EXAMPLE_IMAGE_DIR.joinpath("1.jpg"): "サンプル１",
        EXAMPLE_IMAGE_DIR.joinpath("2.jpg"): "サンプル２",
        EXAMPLE_IMAGE_DIR.joinpath("3.jpg"): "サンプル３",
    }
    example_image_fp = st.selectbox(
        "サンプル画像で仕上がりを確認できます",
        list(image_paths.keys()),
        format_func=lambda x: image_paths[x],
    )



    # スタンプの種類を選択
    emoji = st.selectbox(
        "スタンプの種類を選択してください",
        list(Emoji),
        format_func=lambda x: f"{x.value} {x.name}",  
    )

    page_left, page_right = st.columns([1, 1])
    page_left.subheader("元の画像")
    page_right.subheader("結果")

    image = Image.open(example_image_fp)
    if user_image_fp is not None:
        image = Image.open(user_image_fp)

    page_left.image(image)
    if page_left.button("GO"):
        with st.spinner("編集中"):
            output = get_image_face_hided_by_emoji(image, emoji)
        page_right.image(output)

        buf = BytesIO()
        image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        page_right.download_button(
            label="DOWNLOAD",
            data=byte_im,
            file_name="result.png",
            mime="image/png",
        )


if __name__ == "__main__":
    render()
