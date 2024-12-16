package entities;

import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.util.ArrayList;

import main.Game;
import utilz.LoadSave;

public class FlyingSheep extends Entity {
    // Define Sheep States
    public enum SheepState {
        IDLE,
        FOLLOWING,
        ATTACKING,
        RETURNING
    }

    // Animation Frames
    private BufferedImage[] bouncingSprites;
    private BufferedImage[] idleSprites;

    // Animation Control
    private int aniTick, aniIndex;
    private static final int ANI_SPEED = 25;

    // Movement and Attack Control
    private boolean movingLeft = true;
    private SheepState currentState = SheepState.IDLE;
    private Enemy targetEnemy;

    // Constants
    private static final float FIND_ENEMY_RADIUS = 400f;    // Pixels to search for enemies
    private static final float ATTACK_RANGE = 60f;          // Pixels to attack enemies
    private static final float FOLLOW_DISTANCE = 50f;       // Pixels to trigger following
    private static final float MOVE_SPEED = 0.6f * Game.SCALE;
    private static final float ATTACK_COOLDOWN = 160;       // Frames (e.g., ~3.33 seconds at 60 FPS)
    private int attackCooldownTick = 0;

    public FlyingSheep(float x, float y, int width, int height) {
        super(x, y, width, height);
        loadAnimations();
        initHitbox(20, 20);
    }

    /**
     * Load animation frames from sprite sheets.
     */
    private void loadAnimations() {
        BufferedImage bouncingSheet = LoadSave.GetSpriteAtlas(LoadSave.SHEEP_BOUNCING);
        BufferedImage idleSheet = LoadSave.GetSpriteAtlas(LoadSave.SHEEP_IDLE);
        
        // Initialize sprite arrays
        bouncingSprites = new BufferedImage[6];
        idleSprites = new BufferedImage[8];

        // Extract bouncing sprites
        for (int i = 0; i < bouncingSprites.length; i++) {
            bouncingSprites[i] = bouncingSheet.getSubimage(i * width, 0, width, height);
        }

        // Extract idle sprites
        for (int i = 0; i < idleSprites.length; i++) {
            idleSprites[i] = idleSheet.getSubimage(i * width, 0, width, height);
        }
    }

    /**
     * Update method called every frame to handle animation and behavior.
     * 
     * @param player  The player object to follow.
     * @param enemies The list of active enemies to potentially attack.
     */
    public void update(Player player, ArrayList<Enemy> enemies) {
        handleState(player, enemies);
        handleAnimation();
    }

    /**
     * Handle the current state behavior.
     * 
     * @param player  The player object.
     * @param enemies The list of active enemies.
     */
    private void handleState(Player player, ArrayList<Enemy> enemies) {
        switch (currentState) {
            case IDLE:
                if (playerIsMoving(player) || playerIsWithinDistance(player, FOLLOW_DISTANCE)) {
                    changeState(SheepState.FOLLOWING);
                }
                break;

            case FOLLOWING:
                followPlayer(player);
                targetEnemy = findNearestEnemy(enemies, FIND_ENEMY_RADIUS);
                if (targetEnemy != null) {
                    changeState(SheepState.ATTACKING);
                }
                break;

            case ATTACKING:
                if (targetEnemy != null && targetEnemy.isActive()) {
                    float distanceToEnemy = distanceTo(targetEnemy);
                    if (distanceToEnemy <= ATTACK_RANGE) {
                        attackEnemy();
                    } else if (distanceToEnemy <= FIND_ENEMY_RADIUS) {
                        followTarget(targetEnemy);
                    } else {
                        targetEnemy = null;
                        changeState(SheepState.RETURNING);
                    }
                } else {
                    targetEnemy = null;
                    changeState(SheepState.RETURNING);
                }
                break;

            case RETURNING:
                returnToPlayer(player);
                if (isNearPlayer(player, 10)) { // Near enough to stop
                    changeState(SheepState.IDLE);
                }
                break;
        }
    }

    /**
     * Handle animation frame updates based on time ticks.
     */
    private void handleAnimation() {
        aniTick++;
        if (aniTick >= ANI_SPEED) {
            aniTick = 0;
            aniIndex++;
            BufferedImage[] currentSprites = getCurrentSpriteArray();
            if (aniIndex >= currentSprites.length) {
                aniIndex = 0;
            }
        }
    }

    /**
     * Change the current state of the sheep.
     * 
     * @param newState The new state to transition into.
     */
    private void changeState(SheepState newState) {
        if (currentState != newState) {
            currentState = newState;
            aniTick = 0;
            aniIndex = 0;
        }
    }

    /**
     * Determine if the player is moving.
     * 
     * @param player The player object.
     * @return True if the player is moving, else False.
     */
    private boolean playerIsMoving(Player player) {
        return player.isLeft() || player.isRight();
    }

    /**
     * Determine if the player is within a specific distance.
     * 
     * @param player   The player object.
     * @param distance The distance threshold.
     * @return True if the player is within the distance, else False.
     */
    private boolean playerIsWithinDistance(Player player, float distance) {
        float dx = player.getHitbox().x - hitbox.x;
        float dy = player.getHitbox().y - hitbox.y;
        return Math.hypot(dx, dy) < distance;
    }

    /**
     * Check if the sheep is near the player within a specific distance.
     * 
     * @param player   The player object.
     * @param distance The distance threshold.
     * @return True if near, else False.
     */
    private boolean isNearPlayer(Player player, float distance) {
        return playerIsWithinDistance(player, distance);
    }

    /**
     * Follow the player by moving towards their position.
     * 
     * @param player The player object.
     */
    private void followPlayer(Player player) {
        float dx = player.getHitbox().x - hitbox.x + 50;
        float dy = player.getHitbox().y - hitbox.y - 100; // Offset above the player
        moveTowards(dx, dy);
    }

    /**
     * Follow the targeted enemy by moving towards their position.
     * 
     * @param enemy The target enemy.
     */
    private void followTarget(Enemy enemy) {
        float dx = enemy.getHitbox().x - hitbox.x;
        float dy = enemy.getHitbox().y - hitbox.y;
        moveTowards(dx, dy);
    }

    /**
     * Move towards a target (player or enemy).
     * 
     * @param dx The X offset.
     * @param dy The Y offset.
     */
    private void moveTowards(float dx, float dy) {
        float distance = (float) Math.hypot(dx, dy);
        if (Math.abs(dx) > 5) {
            movingLeft = dx < 0;
        }

        if (distance > 0) {
            float angle = (float) Math.atan2(dy, dx);
            float deltaX = (float) Math.cos(angle) * MOVE_SPEED;
            float deltaY = (float) Math.sin(angle) * MOVE_SPEED;

            hitbox.x += deltaX;
            hitbox.y += deltaY;
        }
    }

    /**
     * Find the nearest active enemy within a specific range.
     * 
     * @param enemies The list of active enemies.
     * @param range   The range to search within.
     * @return The nearest enemy if found, else null.
     */
    private Enemy findNearestEnemy(ArrayList<Enemy> enemies, float range) {
        Enemy nearest = null;
        float minDistance = Float.MAX_VALUE;
        for (Enemy enemy : enemies) {
            if (enemy.isActive()) {
                float distance = distanceTo(enemy);
                if (distance < minDistance && distance <= range) {
                    minDistance = distance;
                    nearest = enemy;
                }
            }
        }
        return nearest;
    }

    /**
     * Calculate the distance to a target enemy.
     * 
     * @param enemy The target enemy.
     * @return The distance in pixels.
     */
    private float distanceTo(Enemy enemy) {
        float dx = enemy.getHitbox().x - hitbox.x;
        float dy = enemy.getHitbox().y - hitbox.y;
        return (float) Math.hypot(dx, dy);
    }

    /**
     * Attack the targeted enemy.
     */
    private void attackEnemy() {
        if (attackCooldownTick > 0) {
            attackCooldownTick--;
            return;
        }

        if (targetEnemy != null && targetEnemy.isActive()) {
            targetEnemy.hurt(3); // Adjust damage as needed
            attackCooldownTick = (int) ATTACK_COOLDOWN;
        }
    }

    /**
     * Return to the player's position by moving towards them.
     * 
     * @param player The player object.
     */
    private void returnToPlayer(Player player) {
        float dx = player.getHitbox().x - hitbox.x;
        float dy = player.getHitbox().y - hitbox.y;
        moveTowards(dx, dy);
    }

    /**
     * Get the current sprite array based on the state.
     * 
     * @return The appropriate sprite array.
     */
    private BufferedImage[] getCurrentSpriteArray() {
        switch (currentState) {
            case IDLE:
                return idleSprites;
            case FOLLOWING:
            case ATTACKING:
            case RETURNING:
                return bouncingSprites;
            default:
                return idleSprites;
        }
    }

    /**
     * Render the FlyingSheep on the screen.
     * 
     * @param g          The Graphics object.
     * @param lvlOffset  The level offset for rendering.
     */
    public void render(Graphics g, int lvlOffset) {
        BufferedImage currentSprite = getCurrentSpriteArray()[aniIndex];
        int drawX = (int) hitbox.x - lvlOffset;
        int drawY = (int) hitbox.y;

        if (movingLeft) {
            g.drawImage(currentSprite, drawX + width - 75, drawY - 50, -width, height, null);
        } else {
            g.drawImage(currentSprite, drawX - 75, drawY - 50, width, height, null);
        }
    }
}
