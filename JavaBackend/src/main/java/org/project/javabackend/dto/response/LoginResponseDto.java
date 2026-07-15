package org.project.javabackend.dto.response;


public record LoginResponseDto(

        String accessToken,
        String refreshToken

) {
}
