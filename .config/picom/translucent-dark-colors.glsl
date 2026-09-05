#version 330
in vec2 texcoord;

uniform sampler2D tex;

vec4 default_post_processing(vec4 c);

vec4 window_shader()
{
    vec4 c = texelFetch(tex, ivec2(texcoord), 0);

    const float luma_start  = 0.20;
    const float luma_end    = 0.10;
    const float opacity_min = 0.8;

    const float luma = max(max(c.r, c.g), c.b);
    const float k = ((luma - luma_end) / (luma_start - luma_end));
    c.a *= clamp(k, opacity_min, 1.0);

    return default_post_processing(c);
}
