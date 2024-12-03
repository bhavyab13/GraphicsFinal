#version 330 core

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoords;

out vec4 FragColor;

uniform vec3 shCoefficients[9];
uniform vec3 baseColor;
uniform vec3 specularColor;
uniform float glossiness;
uniform vec3 viewPos;

vec3 evaluateSH(vec3 normal) {
    float x = normal.x, y = normal.y, z = normal.z;

    vec3 result = vec3(0.0);
    result += shCoefficients[0] * 0.282095;
    result += shCoefficients[1] * (0.488603 * x);
    result += shCoefficients[2] * (0.488603 * y);
    result += shCoefficients[3] * (0.488603 * z);
    result += shCoefficients[4] * (1.092548 * x * z);
    result += shCoefficients[5] * (1.092548 * y * z);
    result += shCoefficients[6] * (0.315392 * (3.0 * z * z - 1.0));
    result += shCoefficients[7] * (1.092548 * x * y);
    result += shCoefficients[8] * (0.546274 * (x * x - y * y));
    return result;
}

vec3 computeSpecular(vec3 normal, vec3 viewDir, vec3 reflectDir) {
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), glossiness);
    return specularColor * spec;
}

void main() {
    vec3 N = normalize(Normal);
    vec3 V = normalize(viewPos - FragPos);
    vec3 R = reflect(-V, N);

    vec3 diffuseLighting = evaluateSH(N);
    vec3 diffuse = baseColor * diffuseLighting;
    vec3 specular = computeSpecular(N, V, R);

    vec3 color = diffuse + specular;

    FragColor = vec4(color, 1.0);
}
