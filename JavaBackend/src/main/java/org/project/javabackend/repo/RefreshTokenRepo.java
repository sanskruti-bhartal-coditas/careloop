package org.project.javabackend.repo;

import org.project.javabackend.entity.RefreshToken;
import org.project.javabackend.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface RefreshTokenRepo extends JpaRepository<RefreshToken,String> {
    Optional<List<RefreshToken>> findAllByUser(User user);
}
